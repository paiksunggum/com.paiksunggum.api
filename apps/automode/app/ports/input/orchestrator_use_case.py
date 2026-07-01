from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any


class OrchestratorUseCase(ABC):
    @abstractmethod
    async def handle(
        self, message: str, contacts: dict[str, str] | None = None
    ) -> dict[str, Any]:
        pass
