from __future__ import annotations
import logging


from apps.titanic.adapter.inbound.api.schemas.crew_lowe_boat_schema import LoweBoatSchema
from apps.titanic.app.dtos.crew_lowe_boat_dto import LoweBoatQuery, LoweBoatResponse
from apps.titanic.app.ports.input.crew_lowe_boat_use_case import LoweBoatUseCase
from apps.titanic.app.ports.output.crew_lowe_boat_port import LoweBoatPort

logger = logging.getLogger("apps")


class LoweBoatInteractor(LoweBoatUseCase):
    
    def __init__(self, repository: LoweBoatPort):
        self.repository = repository

    async def introduce_myself(self, schema: LoweBoatSchema) -> LoweBoatResponse:
        '''해롤드 로우의 자기소개 인터렉트'''
        
        return await self.repository.introduce_myself(LoweBoatQuery(
            id = schema.id,
            name = schema.name
        ))