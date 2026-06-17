from __future__ import annotations
import logging

from apps.titanic.adapter.inbound.api.schemas.crew_andrew_blueprint_schema import AndrewBlueprintSchema
from apps.titanic.app.dtos.crew_andrew_blueprint_dto import AndrewBlueprintQuery, AndrewBlueprintResponse
from apps.titanic.app.ports.input.crew_andrew_blueprint_use_case import AndrewBlueprintUseCase
from apps.titanic.app.ports.output.crew_andrew_blueprint_port import AndrewBlueprintPort

logger = logging.getLogger("apps")

class AndrewBlueprintInteractor(AndrewBlueprintUseCase):
    
    def __init__(self, repository: AndrewBlueprintPort):
        self.repository = repository

    async def get_train_set(self) -> list:
        '''앤드류가 DB에서 train set 만 가져오는 메소드'''
        return await self.repository.get_train_set()

    async def get_test_set(self) -> list:
        '''앤드류가 DB에서 test set 만 가져오는 메소드'''
        return await self.repository.get_test_set()
    

    async def introduce_myself(self, schema: AndrewBlueprintSchema) -> AndrewBlueprintResponse:
        '''앤드류 블루프린트의 자기소개 인터렉트'''
        
        return await self.repository.introduce_myself(AndrewBlueprintQuery(
            id=schema.id,
            name=schema.name,
        ))