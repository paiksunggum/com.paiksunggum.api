from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any

from apps.titanic.adapter.inbound.api.schemas.crew_a_architect_schema import AArchitectSchema
from apps.titanic.app.dtos.crew_a_architect_dto import AArchitectResponse


class AArchitectUseCase(ABC):

    @abstractmethod
    async def introduce_myself(self, schema: AArchitectSchema) -> AArchitectResponse:
        '''토마스 에이 아키텍트의 자기소개 메소드'''
        pass