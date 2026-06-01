from csv import DictReader
from io import StringIO
import logging

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from pydantic import ValidationError

from .....app.ports.input.james_command_use_case import JamesCommandUseCase
from .. import get_james_command_use_case
from ..schemas.james_command_schema import (
    JamesCommandFileUploadResponse,
    JamesCommandSchema,
)

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


@james_router.post("/fileupload", response_model=JamesCommandFileUploadResponse)
async def upload_titanic_csv(
    file: UploadFile = File(...),
    use_case: JamesCommandUseCase = Depends(get_james_command_use_case),
) -> JamesCommandFileUploadResponse:
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

    records = [row.model_dump() for row in passengers]

    # 레코드 목록의 상위 5줄만 출력 (실제 서비스에서는 제거)
    print("라우터에 업로드된 레코드 예시:")
    for record in records[:5]:
        print(record)

    logger.info(
        "[라우터→유스케이스] CSV 업로드 요청 수신 | 파일=%s, 승객 %d행",
        file.filename,
        len(passengers),
    )

    try:
        # 데이터베이스에 저장
        result = await use_case.upload_passengers(records)
        inserted = int(result["inserted"])
        return JamesCommandFileUploadResponse(
            inserted=inserted,
            fileName=file.filename,
            columns=normalized_columns,
            dataRowCount=inserted,
        )
    except RuntimeError as e:
        logger.exception("[라우터] CSV 업로드 실패 | 파일=%s", file.filename)
        raise HTTPException(status_code=503, detail=str(e)) from e
