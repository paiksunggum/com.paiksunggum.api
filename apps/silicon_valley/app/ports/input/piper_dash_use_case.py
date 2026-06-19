from __future__ import annotations

from abc import ABC, abstractmethod

from apps.silicon_valley.adapter.inbound.api.schemas.piper_dash_schema import PiperDashSchema
from apps.silicon_valley.app.dtos.piper_dash_dto import PiperDashResponse


class PiperDashUseCase(ABC):

    @abstractmethod
    async def introduce_myself(self, schema: PiperDashSchema) -> PiperDashResponse:
        '''Pied Piper Dashboard 자기소개 메소드'''
        pass
