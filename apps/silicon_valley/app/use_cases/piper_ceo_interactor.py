from __future__ import annotations
import logging

from apps.silicon_valley.adapter.inbound.api.schemas.piper_ceo_schema import PiperCeoSchema
from apps.silicon_valley.app.dtos.piper_ceo_dto import PiperCeoQuery, PiperCeoResponse
from apps.silicon_valley.app.ports.input.piper_ceo_use_case import PiperCeoUseCase
from apps.silicon_valley.app.ports.output.piper_ceo_port import PiperCeoPort

logger = logging.getLogger("apps")


class PiperCeoInteractor(PiperCeoUseCase):

    def __init__(self, repository: PiperCeoPort):
        self.repository = repository

    async def introduce_myself(self, schema: PiperCeoSchema) -> PiperCeoResponse:
        '''리처드 헨드릭스의 자기소개 인터렉트'''
        return await self.repository.introduce_myself(PiperCeoQuery(
            id=schema.id,
            name=schema.name,
        ))
