from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any

from apps.titanic.app.dtos.crew_james_command_dto import BookingCommand, PersonCommand


class JamesPort(ABC):
    @abstractmethod
    async def upload_passengers(
        person_commands: list[PersonCommand],
        booking_commands: list[BookingCommand],
    ) -> dict[str, Any]:
        pass
