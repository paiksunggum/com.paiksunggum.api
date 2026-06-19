from __future__ import annotations
import logging

from apps.silicon_valley.adapter.inbound.api.schemas.piper_hr_schema import PiperHrSchema
from apps.silicon_valley.app.dtos.piper_hr_dto import PiperHrQuery, PiperHrResponse
from apps.silicon_valley.app.ports.input.piper_hr_use_case import PiperHrUseCase
from apps.silicon_valley.app.ports.output.piper_hr_port import PiperHrPort

logger = logging.getLogger("apps")


class PiperHrInteractor(PiperHrUseCase):

    def __init__(self, repository: PiperHrPort):
        self.repository = repository

    async def introduce_myself(self, schema: PiperHrSchema) -> PiperHrResponse:
        '''HR 매니저의 자기소개 인터렉트'''
        return await self.repository.introduce_myself(PiperHrQuery(
            id=schema.id,
            name=schema.name,
        ))
