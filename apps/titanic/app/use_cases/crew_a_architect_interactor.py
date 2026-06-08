from __future__ import annotations

import logging

from apps.titanic.adapter.inbound.api.schemas.crew_a_architect_schema import AArchitectSchema
from apps.titanic.app.dtos.crew_a_architect_dto import AArchitectQuery, AArchitectResponse
from apps.titanic.app.ports.input.crew_a_architect_use_case import AArchitectUseCase
from apps.titanic.app.ports.output.crew_a_architect_repository import AArchitectRepository

logger = logging.getLogger("apps")


class AArchitectInteractor(AArchitectUseCase):
    
    def __init__(self, repository: AArchitectRepository):
        self.repository = repository

    async def introduce_myself(self, schema: AArchitectSchema) -> AArchitectResponse:
        '''토마스 에이 아키텍트의 자기소개 인터렉트'''
        
        return await self.repository.introduce_myself(AArchitectQuery(
            id = schema.id,
            name = schema.name
        ))
