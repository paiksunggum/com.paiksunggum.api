from __future__ import annotations

from datetime import date

from apps.admin.adapter.inbound.api.schemas.ad_stats_daily_schema import AdStatsDailySchema
from apps.admin.app.dtos.ad_stats_daily_dto import AdStatsDailyQuery, AdStatsDailyResponse
from apps.admin.app.ports.input.ad_stats_daily_use_case import AdStatsDailyUseCase
from apps.admin.app.ports.output.ad_stats_daily_repository import AdStatsDailyRepository


class AdStatsDailyInteractor(AdStatsDailyUseCase):

    def __init__(self, repository: AdStatsDailyRepository):
        self.repository = repository

    async def introduce_myself(self, schema: AdStatsDailySchema) -> AdStatsDailyResponse:
        '''ad_stats_daily 의 자기소개 인터렉트'''

        return await self.repository.introduce_myself(AdStatsDailyQuery(
            ad_id = schema.id,
            stat_date = schema.stat_date,
            impressions = schema.impressions,
            clicks = schema.clicks,
        ))
