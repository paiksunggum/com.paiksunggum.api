from __future__ import annotations
from sqlalchemy.ext.asyncio import AsyncSession

from apps.titanic.app.dtos.crew_a_architect_dto import AArchitectQuery, AArchitectResponse
from apps.titanic.app.ports.output.crew_a_architect_repository import AArchitectRepository
import logging
logger = logging.getLogger("apps")

class AArchitectPgRepository(AArchitectRepository):

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def introduce_myself(self, query: AArchitectQuery) -> AArchitectResponse:
        
        '''월터의 자기 소개 레포지토리 구현 메소드'''

        logger.info(f"[AArchitectPgRepository] introduce_myself 진입 | request_data={query}")
        
        response: AArchitectResponse = AArchitectResponse(
            id= query.id * 10000,
            name= query.name + "가 레포지토리에 다녀옴"
        )
        return response