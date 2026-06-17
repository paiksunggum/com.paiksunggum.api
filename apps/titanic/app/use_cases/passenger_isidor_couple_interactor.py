from __future__ import annotations
import logging

from apps.titanic.adapter.inbound.api.schemas.passenger_isidor_couple_schema import IsidorCoupleSchema
from apps.titanic.app.dtos.passenger_isidor_couple_dto import IsidorCoupleQuery, IsidorCoupleResponse
from apps.titanic.app.ports.input.passenger_isidor_couple_use_case import IsidorCoupleUseCase
from apps.titanic.app.ports.output.passenger_isidor_couple_port import IsidorCouplePort

logger = logging.getLogger("apps")


class IsidorCoupleInteractor(IsidorCoupleUseCase):
    
    def __init__(self, repository: IsidorCouplePort):
        self.repository = repository

    async def introduce_myself(self, schema: IsidorCoupleSchema) -> IsidorCoupleResponse:
        '''이시도르 스트라우스의 자기소개 인터렉트'''
        
        return await self.repository.introduce_myself(IsidorCoupleQuery(
            id = schema.id,
            name = schema.name
        ))
