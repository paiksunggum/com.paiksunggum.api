from __future__ import annotations

import logging

from fastapi import APIRouter, Depends, HTTPException

from apps.automode.adapter.inbound.api.schemas.telegram_schema import (
    TelegramIntroduceResponseSchema,
    TelegramSendRequest,
    TelegramSendResponse,
)
from apps.automode.app.dtos.telegram_dto import (
    TelegramIntroduceQuery,
    TelegramSendCommand,
)
from apps.automode.app.ports.input.telegram_use_case import TelegramUseCase
from apps.automode.dependencies.telegram_provider import get_telegram_use_case

logger = logging.getLogger("apps")
telegram_router = APIRouter(prefix="/telegram", tags=["automode"])


@telegram_router.post("/send", response_model=TelegramSendResponse)
async def send_message(
    body: TelegramSendRequest,
    use_case: TelegramUseCase = Depends(get_telegram_use_case),
) -> TelegramSendResponse:
    logger.info("[automode] 텔레그램 메시지 전송 요청 | text=%s", body.text[:30])
    try:
        result = await use_case.send_message(TelegramSendCommand(text=body.text))
        return TelegramSendResponse(ok=result.ok, message_id=result.message_id)
    except Exception as e:
        logger.exception("[automode] 텔레그램 전송 실패")
        raise HTTPException(status_code=503, detail=str(e)) from e


@telegram_router.get("/myself", response_model=TelegramIntroduceResponseSchema)
async def introduce_myself(
    use_case: TelegramUseCase = Depends(get_telegram_use_case),
) -> TelegramIntroduceResponseSchema:
    logger.info("[automode] Telegram 서비스 자기소개 요청")
    result = await use_case.introduce_myself(
        TelegramIntroduceQuery(id=4, name="Telegram")
    )
    return TelegramIntroduceResponseSchema(id=result.id, name=result.name)
