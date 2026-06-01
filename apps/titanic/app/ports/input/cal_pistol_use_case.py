from abc import ABC, abstractmethod
from typing import Any


class CalPistolUseCase(ABC):
    @abstractmethod
    async def get_pistol() -> dict[str, Any]:
        """권총 조회."""
        ...
