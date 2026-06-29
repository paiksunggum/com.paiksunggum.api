from __future__ import annotations

from abc import ABC, abstractmethod

from apps.automode.domain.entities.email_message import EmailMessage


class IEmailGateway(ABC):
    @abstractmethod
    async def send(self, message: EmailMessage) -> None:
        pass
