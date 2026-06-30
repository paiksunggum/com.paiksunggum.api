from __future__ import annotations

from abc import ABC, abstractmethod

from apps.automode.app.dtos.telegram_dto import (
    TelegramIntroduceQuery,
    TelegramIntroduceResult,
    TelegramSendCommand,
    TelegramSendResult,
)


class ITelegramUseCase(ABC):
    @abstractmethod
    async def introduce_myself(
        self, query: TelegramIntroduceQuery
    ) -> TelegramIntroduceResult:
        """Telegram 서비스 자기소개"""
        pass

    @abstractmethod
    async def send_message(self, command: TelegramSendCommand) -> TelegramSendResult:
        """텔레그램 메시지 전송"""
        pass
