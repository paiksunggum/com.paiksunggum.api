from abc import ABC, abstractmethod
from typing import Any


class IsidorBedRepository(ABC):
    @abstractmethod
    async def get_bed() -> dict[str, Any]:
        ...
