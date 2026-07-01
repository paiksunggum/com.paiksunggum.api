from __future__ import annotations

from abc import ABC, abstractmethod

from apps.automode.app.dtos.receiver_dto import ReceivedEmail, ReceivedEmailCommand


class ReceiverUseCase(ABC):
    @abstractmethod
    async def receive(self, command: ReceivedEmailCommand) -> ReceivedEmail:
        pass

    @abstractmethod
    async def list_emails(self) -> list[ReceivedEmail]:
        pass
