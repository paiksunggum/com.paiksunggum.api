from __future__ import annotations
import logging

from apps.titanic.adapter.inbound.api.schemas.passenger_jack_trainer_schema import JackTrainerSchema
from apps.titanic.app.dtos.passenger_jack_trainer_dto import JackTrainerQuery, JackTrainerResponse
from apps.titanic.app.ports.input.passenger_jack_trainer_use_case import JackTrainerUseCase
from apps.titanic.app.ports.output.passenger_jack_trainer_repository import JackTrainerRepository

logger = logging.getLogger("apps")


class JackTrainerInteractor(JackTrainerUseCase):
    
    def __init__(self, repository: JackTrainerRepository):
        self.repository = repository

    async def introduce_myself(self, schema: JackTrainerSchema) -> JackTrainerResponse:
        '''잭 도슨의 자기소개 인터렉트'''
        
        return await self.repository.introduce_myself(JackTrainerQuery(
            id = schema.id,
            name = schema.name
        ))