from csv import DictReader
from io import StringIO
import logging

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from pydantic import ValidationError
from sqlalchemy.exc import SQLAlchemyError

from .....app.ports.input.james_command_use_case import JamesCommandUseCase
from .....dependencies.james_command import get_james_command_use_case
from ..schemas.james_command_schema import (
    JamesCommandFileUploadResponse,
    JamesCommandSchema,
)

'''
 james_command_router.py
 전설적인 흥행작 <타이타닉>을 연출하여
 "내가 세상의 왕이다!"를 외친 제임스 카메론 감독의 라우터
 완벽주의 성향으로 타이타닉의 모든 세트와 디테일을
 고증한 아키텍처의 총괄 디렉터 역할 수행
'''

james_router = APIRouter(prefix="/titanic/james", tags=["james"])
logger = logging.getLogger("apps")


def _decode_csv_bytes(raw: bytes) -> str:
    for encoding in ("utf-8-sig", "cp949"):
        try:
            return raw.decode(encoding)
        except UnicodeDecodeError:
            continue
    raise HTTPException(status_code=400, detail="CSV 인코딩을 읽을 수 없습니다.")


def _normalize_header(header: str) -> str:
    lowered = header.strip().lower()
    if lowered in {"sex", "성별"}:
        return "gender"
    return header.strip()


def _require_csv_upload(filename: str | None, raw: bytes) -> str:
    if not filename:
        raise HTTPException(status_code=400, detail="파일 이름이 없습니다.")
    if not filename.lower().endswith(".csv"):
        raise HTTPException(status_code=400, detail="CSV 파일만 업로드할 수 있습니다.")
    if not raw:
        raise HTTPException(status_code=400, detail="빈 파일입니다.")
    return filename


def _parse_titanic_csv(
    raw: bytes,
) -> tuple[list[JamesCommandSchema], list[str]]:
    csv_text = _decode_csv_bytes(raw)
    reader = DictReader(StringIO(csv_text))

    if not reader.fieldnames:
        raise HTTPException(status_code=400, detail="CSV 헤더를 찾을 수 없습니다.")

    normalized_columns = [_normalize_header(name) for name in reader.fieldnames]
    passengers: list[JamesCommandSchema] = []

    for row_num, source_row in enumerate(reader, start=2):
        normalized_row: dict[str, str] = {}
        for original_key, value in source_row.items():
            if original_key is None:
                continue
            normalized_row[_normalize_header(original_key)] = value or ""
        try:
            passengers.append(JamesCommandSchema.model_validate(normalized_row))
        except ValidationError as e:
            raise HTTPException(
                status_code=400,
                detail=f"CSV {row_num}행 형식 오류: {e.errors()[0]['msg']}",
            ) from e

    return passengers, normalized_columns


def _log_passenger_samples(passengers: list[JamesCommandSchema]) -> None:
    logger.info("[제임스 라우터] 업로드 CSV → 스키마 변환 상위 5개 레코드 예시")
    for record in passengers[:5]:
        logger.info("%s", record.model_dump(by_alias=True))


@james_router.post("/fileupload", response_model=JamesCommandFileUploadResponse)
async def upload_titanic_csv(
    file: UploadFile = File(...),
    james: JamesCommandUseCase = Depends(get_james_command_use_case),
) -> JamesCommandFileUploadResponse:
    raw = await file.read()
    filename = _require_csv_upload(file.filename, raw)
    passengers, normalized_columns = _parse_titanic_csv(raw)
    _log_passenger_samples(passengers)

    try:
        result = await james.upload_passengers(passengers)
        inserted = int(result["inserted"])
        return JamesCommandFileUploadResponse(
            inserted=inserted,
            fileName=filename,
            columns=normalized_columns,
            dataRowCount=inserted,
        )
    except RuntimeError as e:
        logger.exception("[제임스 라우터] CSV 업로드 실패 | 파일=%s", filename)
        raise HTTPException(status_code=503, detail=str(e)) from e
    except SQLAlchemyError as e:
        logger.exception("[제임스 라우터] DB 저장 실패 | 파일=%s", filename)
        raise HTTPException(
            status_code=500,
            detail=f"DB 저장에 실패했습니다: {getattr(e, 'orig', e)}",
        ) from e
