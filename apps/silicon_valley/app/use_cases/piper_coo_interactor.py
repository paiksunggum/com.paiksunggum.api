from __future__ import annotations
import logging

from apps.silicon_valley.adapter.inbound.api.schemas.piper_coo_schema import PiperCooSchema
from apps.silicon_valley.app.dtos.piper_coo_dto import PiperCooQuery, PiperCooResponse
from apps.silicon_valley.app.ports.input.piper_coo_use_case import PiperCooUseCase
from apps.silicon_valley.app.ports.output.piper_coo_port import PiperCooPort

logger = logging.getLogger("apps")


class PiperCooInteractor(PiperCooUseCase):

    def __init__(self, repository: PiperCooPort):
        self.repository = repository

    async def introduce_myself(self, schema: PiperCooSchema) -> PiperCooResponse:
        '''재러드 던의 자기소개 인터렉트'''
        return await self.repository.introduce_myself(PiperCooQuery(
            id=schema.id,
            name=schema.name,
        ))
