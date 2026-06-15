from __future__ import annotations

import logging

logger = logging.getLogger(__name__)
from sqlalchemy.ext.asyncio import AsyncSession

from apps.admin.app.dtos.practice_dto import PracticeQuery, PracticeResponse
from apps.admin.app.ports.output.practice_repository import PracticeRepository


class PracticePgRepository(PracticeRepository):
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def introduce_myself(self, query: PracticeQuery) -> PracticeResponse:

        '''practice 의 자기 소개 레포지토리 구현 메소드'''

        logger.info(f"[PracticePgRepository] introduce_myself 진입 | request_data={query}")

        response: PracticeResponse = PracticeResponse(
            id=query.sports_id * 10000,
            sports_id=query.sports_id,
            title=query.title + "가 레포지토리에 다녀옴",
            description=query.description,
            guide_json=query.guide_json,
            is_active=query.is_active,
            created_at=None,
        )
        return response
