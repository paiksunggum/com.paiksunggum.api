from __future__ import annotations
import logging

from apps.titanic.adapter.inbound.api.schemas.crew_smith_captain_schema import SmithCaptainSchema
from apps.titanic.app.dtos.crew_smith_captain_dto import SmithCaptainQuery, SmithCaptainResponse
from apps.titanic.app.ports.input.crew_smith_captain_use_case import SmithCaptainUseCase
from apps.titanic.app.ports.output.crew_smith_captain_repository import SmithCaptainRepository

logger = logging.getLogger("apps")


class SmithCaptainInteractor(SmithCaptainUseCase):
    
    def __init__(self, repository: SmithCaptainRepository):
        self.repository = repository

    async def introduce_myself(self, schema: SmithCaptainSchema) -> SmithCaptainResponse:
        '''에드워드 스미스의 자기소개 인터렉트'''
        
        return await self.repository.introduce_myself(SmithCaptainQuery(
            id = schema.id,
            name = schema.name
        ))




