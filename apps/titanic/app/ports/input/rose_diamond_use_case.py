from abc import ABC, abstractmethod
from typing import Any


class RoseDiamondUseCase(ABC):
    @abstractmethod
    async def get_diamond() -> dict[str, Any]:
        """다이아몬드 조회."""
        ...
