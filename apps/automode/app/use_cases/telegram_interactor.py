from __future__ import annotations

from apps.automode.app.dtos.telegram_dto import (
    TelegramIntroduceQuery,
    TelegramIntroduceResult,
    TelegramSendCommand,
    TelegramSendResult,
)
from apps.automode.app.ports.input.telegram_use_case import TelegramUseCase
from apps.automode.app.ports.output.telegram_port import TelegramPort


class TelegramInteractor(TelegramUseCase):
    def __init__(self, repository: TelegramPort) -> None:
        self._repository = repository

    async def introduce_myself(
        self, query: TelegramIntroduceQuery
    ) -> TelegramIntroduceResult:
        return await self._repository.introduce_myself(query)

    async def send_message(self, command: TelegramSendCommand) -> TelegramSendResult:
        return await self._repository.send_message(command)
