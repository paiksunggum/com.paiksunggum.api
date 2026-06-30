from __future__ import annotations

from apps.automode.app.dtos.telegram_dto import (
    TelegramIntroduceQuery,
    TelegramIntroduceResult,
    TelegramSendCommand,
    TelegramSendResult,
)
from apps.automode.app.ports.input.i_telegram_use_case import ITelegramUseCase
from apps.automode.app.ports.output.i_telegram_port import ITelegramPort


class TelegramInteractor(ITelegramUseCase):
    def __init__(self, repository: ITelegramPort) -> None:
        self._repository = repository

    async def introduce_myself(
        self, query: TelegramIntroduceQuery
    ) -> TelegramIntroduceResult:
        return await self._repository.introduce_myself(query)

    async def send_message(self, command: TelegramSendCommand) -> TelegramSendResult:
        return await self._repository.send_message(command)
