from abc import ABC, abstractmethod
from typing import Any


class RuthCorsetRepository(ABC):
    @abstractmethod
    async def get_corset() -> dict[str, Any]:
        ...
