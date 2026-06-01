from abc import ABC, abstractmethod
from typing import Any


class AndrewBlueprintRepository(ABC):
    @abstractmethod
    async def get_blueprint() -> dict[str, Any]:
        ...
