from abc import ABC, abstractmethod
from typing import Any


class SmithCaptainUseCase(ABC):
    @abstractmethod
    async def get_captain() -> dict[str, Any]:
        """선장 조회."""
        ...
