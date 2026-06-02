from abc import ABC, abstractmethod
from typing import Any

from apps.titanic.adapter.inbound.api.schemas.james_command_schema import (
    JamesCommandSchema,
)


class JamesCommandUseCase(ABC):
    @abstractmethod
    async def upload_passengers(
        passengers: list[JamesCommandSchema],
    ) -> dict[str, Any]:
        ...
