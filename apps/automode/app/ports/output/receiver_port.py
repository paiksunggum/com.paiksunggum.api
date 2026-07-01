from __future__ import annotations

from abc import ABC, abstractmethod

from apps.automode.app.dtos.receiver_dto import ReceivedEmail, ReceivedEmailCommand


class ReceiverPort(ABC):
    @abstractmethod
    async def save(self, command: ReceivedEmailCommand) -> ReceivedEmail:
        pass

    @abstractmethod
    async def find_all(self) -> list[ReceivedEmail]:
        pass
