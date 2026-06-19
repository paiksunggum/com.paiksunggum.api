from __future__ import annotations

from abc import ABC, abstractmethod

from apps.silicon_valley.adapter.inbound.api.schemas.piper_sys_schema import PiperSysSchema
from apps.silicon_valley.app.dtos.piper_sys_dto import PiperSysResponse


class PiperSysUseCase(ABC):

    @abstractmethod
    async def introduce_myself(self, schema: PiperSysSchema) -> PiperSysResponse:
        '''Pied Piper Systems Architect 자기소개 메소드'''
        pass
