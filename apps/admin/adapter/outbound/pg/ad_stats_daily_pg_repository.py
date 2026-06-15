from __future__ import annotations

import logging

logger = logging.getLogger(__name__)
from sqlalchemy.ext.asyncio import AsyncSession

from apps.admin.app.dtos.ad_stats_daily_dto import AdStatsDailyQuery, AdStatsDailyResponse
from apps.admin.app.ports.output.ad_stats_daily_repository import AdStatsDailyRepository

class AdStatsDailyPgRepository(AdStatsDailyRepository):
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def introduce_myself(self, query: AdStatsDailyQuery) -> AdStatsDailyResponse:

        '''ad_stats_daily 의 자기 소개 레포지토리 구현 메소드'''

        logger.info(f"[AdStatsDailyPgRepository] introduce_myself 진입 | request_data={query}")

        response: AdStatsDailyResponse = AdStatsDailyResponse(
            id=query.ad_id * 10000,
            ad_id=query.ad_id,
            stat_date=query.stat_date,
            impressions=query.impressions,
            clicks=query.clicks,
            created_at=None,
        )
        return response
