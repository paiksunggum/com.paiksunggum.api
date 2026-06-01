from abc import ABC, abstractmethod
from typing import Any


class HartleyViolinUseCase(ABC):
    @abstractmethod
    async def get_violin() -> dict[str, Any]:
        """바이올린 조회."""
        ...
