from abc import ABC, abstractmethod
from typing import Any


class IsidorBedUseCase(ABC):
    @abstractmethod
    async def get_bed() -> dict[str, Any]:
        """침대 조회."""
        ...
