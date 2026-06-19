from __future__ import annotations
import logging

from apps.silicon_valley.adapter.inbound.api.schemas.piper_dash_schema import PiperDashSchema
from apps.silicon_valley.app.dtos.piper_dash_dto import PiperDashQuery, PiperDashResponse
from apps.silicon_valley.app.ports.input.piper_dash_use_case import PiperDashUseCase
from apps.silicon_valley.app.ports.output.piper_dash_port import PiperDashPort

logger = logging.getLogger("apps")


class PiperDashInteractor(PiperDashUseCase):

    def __init__(self, repository: PiperDashPort):
        self.repository = repository

    async def introduce_myself(self, schema: PiperDashSchema) -> PiperDashResponse:
        '''모니카 홀의 자기소개 인터렉트'''
        return await self.repository.introduce_myself(PiperDashQuery(
            id=schema.id,
            name=schema.name,
        ))
