from __future__ import annotations
import logging

from apps.titanic.adapter.inbound.api.schemas.crew_andrew_blueprint_schema import AndrewBlueprintSchema
from apps.titanic.app.dtos.crew_andrew_blueprint_dto import AndrewBlueprintQuery, AndrewBlueprintResponse
from apps.titanic.app.ports.input.crew_andrew_blueprint_use_case import AndrewBlueprintUseCase
from apps.titanic.app.ports.output.crew_andrew_blueprint_repository import AndrewBlueprintRepository

logger = logging.getLogger("apps")

class AndrewBlueprintInteractor(AndrewBlueprintUseCase):
    
    def __init__(self, repository: AndrewBlueprintRepository):
        self.repository = repository

    async def introduce_myself(self, schema: AndrewBlueprintSchema) -> AndrewBlueprintResponse:
        '''앤드류 블루프린트의 자기소개 인터렉트'''
        
        return await self.repository.introduce_myself(AndrewBlueprintQuery(
            id=schema.id,
            name=schema.name,
        ))