from __future__ import annotations

from abc import ABC, abstractmethod

from apps.automode.app.dtos.email_request_dto import EmailSendCommand, EmailSendResult


class IEmailSendUseCase(ABC):
    @abstractmethod
    async def send(self, command: EmailSendCommand) -> EmailSendResult:
        pass
