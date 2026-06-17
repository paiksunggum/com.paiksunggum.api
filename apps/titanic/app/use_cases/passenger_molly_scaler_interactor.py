from __future__ import annotations
import logging

from apps.titanic.adapter.inbound.api.schemas.passenger_molly_scaler_schema import MollyScalerSchema
from apps.titanic.app.dtos.passenger_molly_scaler_dto import MollyScalerQuery, MollyScalerResponse
from apps.titanic.app.ports.input.passenger_molly_scaler_use_case import MollyScalerUseCase
from apps.titanic.app.ports.output.passenger_molly_scaler_port import MollyScalerPort

logger = logging.getLogger("apps")

class MollyScalerInteractor(MollyScalerUseCase):
    
    def __init__(self, repository: MollyScalerPort):
        self.repository = repository

    async def introduce_myself(self, schema: MollyScalerSchema) -> MollyScalerResponse:
        '''몰리 브라운의 자기소개 인터렉트'''
        
        return await self.repository.introduce_myself(MollyScalerQuery(
            id = schema.id,
            name = schema.name
        ))