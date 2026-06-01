from abc import ABC, abstractmethod
from typing import Any


class AndrewBlueprintUseCase(ABC):
    @abstractmethod
    async def get_blueprint() -> dict[str, Any]:
        """설계도 조회."""
        ...
