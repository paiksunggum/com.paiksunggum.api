from __future__ import annotations

import logging
import os

import httpx

from apps.automode.app.dtos.telegram_dto import (
    TelegramIntroduceQuery,
    TelegramIntroduceResult,
    TelegramSendCommand,
    TelegramSendResult,
)
from apps.automode.app.ports.output.i_telegram_port import ITelegramPort

logger = logging.getLogger("apps")

_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")
_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "")
_API_BASE = "https://api.telegram.org"


class TelegramClient(ITelegramPort):

    async def introduce_myself(
        self, query: TelegramIntroduceQuery
    ) -> TelegramIntroduceResult:
        return TelegramIntroduceResult(id=query.id, name="Telegram 봇 서비스")

    async def send_message(self, command: TelegramSendCommand) -> TelegramSendResult:
        url = f"{_API_BASE}/bot{_TOKEN}/sendMessage"
        async with httpx.AsyncClient(timeout=10) as client:
            res = await client.post(
                url,
                json={"chat_id": _CHAT_ID, "text": command.text},
            )
            res.raise_for_status()
            data = res.json()
            logger.info(
                "[TelegramClient] 메시지 전송 완료 | message_id=%s",
                data["result"]["message_id"],
            )
            return TelegramSendResult(
                ok=True, message_id=data["result"]["message_id"]
            )
