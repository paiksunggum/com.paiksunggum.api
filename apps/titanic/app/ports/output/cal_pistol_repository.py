from abc import ABC, abstractmethod
from typing import Any


class CalPistolRepository(ABC):
    @abstractmethod
    async def get_pistol() -> dict[str, Any]:
        ...
