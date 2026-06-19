from __future__ import annotations

from abc import ABC, abstractmethod

from apps.silicon_valley.adapter.inbound.api.schemas.piper_coo_schema import PiperCooSchema
from apps.silicon_valley.app.dtos.piper_coo_dto import PiperCooResponse


class PiperCooUseCase(ABC):

    @abstractmethod
    async def introduce_myself(self, schema: PiperCooSchema) -> PiperCooResponse:
        '''Pied Piper COO 자기소개 메소드'''
        pass
