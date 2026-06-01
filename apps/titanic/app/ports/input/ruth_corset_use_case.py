from abc import ABC, abstractmethod
from typing import Any


class RuthCorsetUseCase(ABC):
    @abstractmethod
    async def get_corset() -> dict[str, Any]:
        """코르셋 조회."""
        ...
