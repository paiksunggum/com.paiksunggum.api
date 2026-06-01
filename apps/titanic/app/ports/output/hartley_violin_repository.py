from abc import ABC, abstractmethod
from typing import Any


class HartleyViolinRepository(ABC):
    @abstractmethod
    async def get_violin() -> dict[str, Any]:
        ...
