from __future__ import annotations

import logging

logger = logging.getLogger(__name__)
from sqlalchemy.ext.asyncio import AsyncSession

from apps.admin.app.dtos.sports_dto import SportsQuery, SportsResponse
from apps.admin.app.ports.output.sports_repository import SportsRepository


class SportsPgRepository(SportsRepository):
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def introduce_myself(self, query: SportsQuery) -> SportsResponse:

        '''sports 의 자기 소개 레포지토리 구현 메소드'''

        logger.info(f"[SportsPgRepository] introduce_myself 진입 | request_data={query}")

        response: SportsResponse = SportsResponse(
            id=1,
            name=query.name + "가 레포지토리에 다녀옴",
            description=query.description,
            is_active=query.is_active,
            created_at=None,
        )
        return response
