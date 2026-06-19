from __future__ import annotations

from abc import ABC, abstractmethod

from apps.silicon_valley.adapter.inbound.api.schemas.piper_ceo_schema import PiperCeoSchema
from apps.silicon_valley.app.dtos.piper_ceo_dto import PiperCeoResponse


class PiperCeoUseCase(ABC):

    @abstractmethod
    async def introduce_myself(self, schema: PiperCeoSchema) -> PiperCeoResponse:
        '''Pied Piper CEO 자기소개 메소드'''
        pass
