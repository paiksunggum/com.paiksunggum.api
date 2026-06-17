from __future__ import annotations
import logging

from apps.titanic.adapter.inbound.api.schemas.passenger_ruth_validation_schema import RuthValidationSchema
from apps.titanic.app.dtos.passenger_ruth_validation_dto import RuthValidationQuery, RuthValidationResponse
from apps.titanic.app.ports.input.passenger_ruth_validation_use_case import RuthValidationUseCase
from apps.titanic.app.ports.output.passenger_ruth_validation_port import RuthValidationPort

logger = logging.getLogger("apps")


class RuthValidationInteractor(RuthValidationUseCase):
    
    def __init__(self, repository: RuthValidationPort):
        self.repository = repository

    async def introduce_myself(self, schema: RuthValidationSchema) -> RuthValidationResponse:
        '''루쓰 드윗 부카터의 자기소개 인터렉트'''
        
        return await self.repository.introduce_myself(RuthValidationQuery(
            id = schema.id,
            name = schema.name
        ))
