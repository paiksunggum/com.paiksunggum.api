from abc import ABC, abstractmethod
from typing import Any


class JackSketchRepository(ABC):
    @abstractmethod
    async def get_sketch() -> dict[str, Any]:
        ...
