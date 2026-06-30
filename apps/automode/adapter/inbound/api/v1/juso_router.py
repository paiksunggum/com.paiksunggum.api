from __future__ import annotations

import logging
import re
from csv import DictReader
from io import StringIO

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from pydantic import ValidationError
from sqlalchemy.exc import SQLAlchemyError

from apps.automode.adapter.inbound.api.schemas.juso_schema import (
    JusoContactItemSchema,
    JusoContactSchema,
    JusoContactUploadResponse,
    JusoIntroduceResponseSchema,
)
from apps.automode.app.dtos.juso_dto import (
    JusoContactCommand,
    JusoIntroduceQuery,
)
from apps.automode.app.ports.input.i_juso_use_case import IJusoUseCase
from apps.automode.dependencies.juso_provider import get_juso_use_case

logger = logging.getLogger("apps")
juso_router = APIRouter(prefix="/juso", tags=["automode"])


# ── CSV 파싱 헬퍼 ──────────────────────────────────────────


def _decode_csv_bytes(raw: bytes) -> str:
    for encoding in ("utf-8-sig", "cp949"):
        try:
            return raw.decode(encoding)
        except UnicodeDecodeError:
            continue
    raise HTTPException(status_code=400, detail="CSV 인코딩을 읽을 수 없습니다.")


def _normalize_header(header: str) -> str:
    """Google 주소록 CSV 헤더를 snake_case 필드명으로 변환.

    예) "E-mail 1 - Value" → "email_1_value"
        "First Name"       → "first_name"
    """
    s = header.strip()
    s = s.replace(" - ", "_")
    s = s.replace("-", "")
    s = re.sub(r"\s+", "_", s)
    s = re.sub(r"[^\w]", "", s)
    return s.lower()


def _require_csv_upload(filename: str | None, raw: bytes) -> str:
    if not filename:
        raise HTTPException(status_code=400, detail="파일 이름이 없습니다.")
    if not filename.lower().endswith(".csv"):
        raise HTTPException(status_code=400, detail="CSV 파일만 업로드할 수 있습니다.")
    if not raw:
        raise HTTPException(status_code=400, detail="빈 파일입니다.")
    return filename


def _parse_contacts_csv(
    raw: bytes,
) -> tuple[list[JusoContactSchema], list[str]]:
    csv_text = _decode_csv_bytes(raw)
    reader = DictReader(StringIO(csv_text))

    if not reader.fieldnames:
        raise HTTPException(status_code=400, detail="CSV 헤더를 찾을 수 없습니다.")

    normalized_columns = [_normalize_header(h) for h in reader.fieldnames]
    contacts: list[JusoContactSchema] = []

    for row_num, source_row in enumerate(reader, start=2):
        normalized_row: dict[str, str] = {}
        for original_key, value in source_row.items():
            if original_key is None:
                continue
            normalized_row[_normalize_header(original_key)] = value or ""
        try:
            contacts.append(JusoContactSchema.model_validate(normalized_row))
        except ValidationError as e:
            raise HTTPException(
                status_code=400,
                detail=f"CSV {row_num}행 형식 오류: {e.errors()[0]['msg']}",
            ) from e

    return contacts, normalized_columns


def _log_contact_samples(contacts: list[JusoContactSchema]) -> None:
    logger.info("[주소록 라우터] 업로드 CSV → 스키마 변환 상위 5개 레코드")
    for record in contacts[:5]:
        logger.info("%s", record.model_dump())


# ── 엔드포인트 ────────────────────────────────────────────


@juso_router.get("/contacts", response_model=list[JusoContactItemSchema])
async def get_contacts(
    use_case: IJusoUseCase = Depends(get_juso_use_case),
) -> list[JusoContactItemSchema]:
    items = await use_case.list_contacts()
    return [JusoContactItemSchema(name=i.name, email=i.email) for i in items]


@juso_router.get("/myself", response_model=JusoIntroduceResponseSchema)
async def introduce_myself(
    use_case: IJusoUseCase = Depends(get_juso_use_case),
) -> JusoIntroduceResponseSchema:
    logger.info("[automode] 주소 검색 서비스 자기소개 요청")
    result = await use_case.introduce_myself(JusoIntroduceQuery(id=3, name="주소검색"))
    return JusoIntroduceResponseSchema(id=result.id, name=result.name)


@juso_router.post("/contacts/upload", response_model=JusoContactUploadResponse)
async def upload_contacts_csv(
    file: UploadFile = File(...),
    use_case: IJusoUseCase = Depends(get_juso_use_case),
) -> JusoContactUploadResponse:
    raw = await file.read()
    filename = _require_csv_upload(file.filename, raw)
    contacts, normalized_columns = _parse_contacts_csv(raw)
    _log_contact_samples(contacts)

    commands = [
        JusoContactCommand(
            first_name=c.first_name or "",
            middle_name=c.middle_name or "",
            last_name=c.last_name or "",
            nickname=c.nickname or "",
            organization_name=c.organization_name or "",
            organization_title=c.organization_title or "",
            birthday=c.birthday or "",
            labels=c.labels or "",
            email=c.email_1_value or "",
            phone=c.phone_1_value or "",
        )
        for c in contacts
    ]

    try:
        result = await use_case.upload_contacts(commands)
        return JusoContactUploadResponse(
            inserted=result.inserted,
            file_name=filename,
            columns=normalized_columns,
            data_row_count=result.inserted,
        )
    except RuntimeError as e:
        logger.exception("[주소록 라우터] CSV 업로드 실패 | 파일=%s", filename)
        raise HTTPException(status_code=503, detail=str(e)) from e
    except SQLAlchemyError as e:
        logger.exception("[주소록 라우터] DB 저장 실패 | 파일=%s", filename)
        raise HTTPException(
            status_code=500,
            detail=f"DB 저장에 실패했습니다: {getattr(e, 'orig', e)}",
        ) from e
