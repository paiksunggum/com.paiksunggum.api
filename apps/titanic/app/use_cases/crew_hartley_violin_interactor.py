from __future__ import annotations
import logging

from apps.titanic.adapter.inbound.api.schemas.crew_hartley_violin_schema import HartleyViolinSchema
from apps.titanic.app.dtos.crew_hartley_violin_dto import HartleyViolinQuery, HartleyViolinResponse
from apps.titanic.app.ports.input.crew_hartley_violin_use_case import HartleyViolinUseCase
from apps.titanic.app.ports.output.crew_hartley_violin_repository import HartleyViolinRepository

logger = logging.getLogger("apps")

class HartleyViolinInteractor(HartleyViolinUseCase):
    
    def __init__(self, repository: HartleyViolinRepository):
        self.repository = repository

    async def introduce_myself(self, schema: HartleyViolinSchema) -> HartleyViolinResponse:
        '''왈리스 하틀리의 자기소개 인터렉트'''
        
        return await self.repository.introduce_myself(HartleyViolinQuery(
            id = schema.id,
            name = schema.name
        ))