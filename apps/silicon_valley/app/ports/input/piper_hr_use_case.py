from __future__ import annotations

from abc import ABC, abstractmethod

from apps.silicon_valley.adapter.inbound.api.schemas.piper_hr_schema import PiperHrSchema
from apps.silicon_valley.app.dtos.piper_hr_dto import PiperHrResponse


class PiperHrUseCase(ABC):

    @abstractmethod
    async def introduce_myself(self, schema: PiperHrSchema) -> PiperHrResponse:
        '''Pied Piper HR 자기소개 메소드'''
        pass
