from __future__ import annotations
import logging

from apps.silicon_valley.adapter.inbound.api.schemas.piper_sys_schema import PiperSysSchema
from apps.silicon_valley.app.dtos.piper_sys_dto import PiperSysQuery, PiperSysResponse
from apps.silicon_valley.app.ports.input.piper_sys_use_case import PiperSysUseCase
from apps.silicon_valley.app.ports.output.piper_sys_port import PiperSysPort

logger = logging.getLogger("apps")


class PiperSysInteractor(PiperSysUseCase):

    def __init__(self, repository: PiperSysPort):
        self.repository = repository

    async def introduce_myself(self, schema: PiperSysSchema) -> PiperSysResponse:
        '''버트람 길포일의 자기소개 인터렉트'''
        return await self.repository.introduce_myself(PiperSysQuery(
            id=schema.id,
            name=schema.name,
        ))
