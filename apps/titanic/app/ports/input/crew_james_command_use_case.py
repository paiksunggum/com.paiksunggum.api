from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any

from apps.titanic.adapter.inbound.api.schemas.crew_james_command_schema import JamesCommandSchema
from apps.titanic.app.dtos.crew_james_command_dto import JamesCommandResponse


class JamesCommandUseCase(ABC):
    @abstractmethod
    async def upload_passengers(
        passengers: list[JamesCommandSchema],
    ) -> dict[str, Any]:
        """CSV 승객 목록을 DB에 저장한다."""
        pass


    @abstractmethod
    async def introduce_myself(self,
        schema: JamesCommandSchema,
    ) -> JamesCommandResponse:
        '''제임스 감독의 자기소개 메소드'''
        pass

