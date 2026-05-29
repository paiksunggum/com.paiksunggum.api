from abc import ABC, abstractmethod
from typing import Any


class JamesRepository(ABC):
    @abstractmethod
    async def upload_passengers(
        records: list[dict[str, Any]],
    ) -> dict[str, Any]:
        ...
