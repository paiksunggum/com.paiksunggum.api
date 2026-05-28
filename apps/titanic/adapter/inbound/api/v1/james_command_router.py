from csv import DictReader
from io import StringIO
import logging

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile

from database import engine

from .....app.ports.input.james_command_use_case import (
    JamesCommandUseCase,
    JamesCommandUseCaseImpl,
)
from .....app.ports.output.james_repository import InMemoryJamesRepository
from .....app.use_cases.james_command import JamesCommand
from ....outbound.pg.james_pg_repository import JamesPgRepository

james_router = APIRouter(prefix="/titanic/james", tags=["james"])
logger = logging.getLogger("apps")


def get_james_repository():
    if engine is not None:
        return JamesPgRepository()
    return InMemoryJamesRepository()


def get_james_command_use_case(
    repository=Depends(get_james_repository),
) -> JamesCommandUseCase:
    return JamesCommandUseCaseImpl(JamesCommand(repository))


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


@james_router.post("/fileupload")
async def upload_titanic_csv(
    file: UploadFile = File(...),
    use_case: JamesCommandUseCase = Depends(get_james_command_use_case),
):
    if not file.filename:
        raise HTTPException(status_code=400, detail="파일 이름이 없습니다.")
    if not file.filename.lower().endswith(".csv"):
        raise HTTPException(status_code=400, detail="CSV 파일만 업로드할 수 있습니다.")

    raw = await file.read()
    if not raw:
        raise HTTPException(status_code=400, detail="빈 파일입니다.")

    csv_text = _decode_csv_bytes(raw)
    reader = DictReader(StringIO(csv_text))

    if not reader.fieldnames:
        raise HTTPException(status_code=400, detail="CSV 헤더를 찾을 수 없습니다.")

    normalized_columns = [_normalize_header(name) for name in reader.fieldnames]

    rows = []
    for source_row in reader:
        normalized_row = {}
        for original_key, value in source_row.items():
            if original_key is None:
                continue
            normalized_row[_normalize_header(original_key)] = value
        rows.append(normalized_row)
    logger.info(
        "[JamesRouter] upload accepted - file=%s, rows=%d",
        file.filename,
        len(rows),
    )

    try:
        result = await use_case.upload_passengers(
            file_name=file.filename,
            columns=normalized_columns,
            rows=rows,
        )
        logger.info(
            "[JamesRouter] upload completed - file=%s, stored_in=%s, rows=%d",
            file.filename,
            result.get("storedIn"),
            result.get("rowCount", 0),
        )
        return result
    except RuntimeError as e:
        logger.exception("[JamesRouter] upload failed - file=%s", file.filename)
        raise HTTPException(status_code=503, detail=str(e)) from e
