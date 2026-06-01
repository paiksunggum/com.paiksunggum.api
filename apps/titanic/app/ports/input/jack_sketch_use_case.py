from abc import ABC, abstractmethod
from typing import Any


class JackSketchUseCase(ABC):
    @abstractmethod
    async def get_sketch() -> dict[str, Any]:
        """스케치 조회."""
        ...
