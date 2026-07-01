from __future__ import annotations

from abc import ABC, abstractmethod

from apps.automode.app.dtos.email_request_dto import (
    EmailClassifyCommand,
    EmailClassifyResult,
)


class EmailClassifyUseCase(ABC):
    @abstractmethod
    async def classify(self, command: EmailClassifyCommand) -> EmailClassifyResult:
        pass
