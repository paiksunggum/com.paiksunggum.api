from __future__ import annotations

import logging

logger = logging.getLogger(__name__)
from sqlalchemy.ext.asyncio import AsyncSession

from apps.admin.app.dtos.ads_dto import AdsQuery, AdsResponse
from apps.admin.app.ports.output.ads_repository import AdsRepository


class AdsPgRepository(AdsRepository):
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def introduce_myself(self, query: AdsQuery) -> AdsResponse:

        '''ads 의 자기 소개 레포지토리 구현 메소드'''

        logger.info(f"[AdsPgRepository] introduce_myself 진입 | request_data={query}")

        response: AdsResponse = AdsResponse(
            id=1,
            title=query.title + "가 레포지토리에 다녀옴",
            image_url=query.image_url,
            target_url=query.target_url,
            budget=query.budget,
            status=query.status,
            created_at=None,
        )
        return response
