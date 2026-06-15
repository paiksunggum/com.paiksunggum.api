from datetime import date

from fastapi import APIRouter, Depends, Query

from apps.admin.adapter.inbound.api.schemas.ad_stats_daily_schema import AdStatsDailySchema
from apps.admin.app.dtos.ad_stats_daily_dto import AdStatsDailyResponse
from apps.admin.app.ports.input.ad_stats_daily_use_case import AdStatsDailyUseCase
from apps.admin.dependencies.ad_stats_daily_provider import get_ad_stats_daily_use_case

'''
콜 성과 분석관 — 일별 광고 노출·클릭 집계 광고 ID와 기간으로 일간 통계를 조회합니다.
'''

ad_stats_daily_router = APIRouter(prefix="/admin/ad-stats-daily", tags=["ad-stats-daily"])


@ad_stats_daily_router.get("/myself")
async def introduce_myself(
    ad_stats_daily: AdStatsDailyUseCase = Depends(get_ad_stats_daily_use_case),
) -> AdStatsDailyResponse:
    return await ad_stats_daily.introduce_myself(
        AdStatsDailySchema(
            id=1,
            ad_id=1,
            stat_date=date(2026, 6, 15),
            impressions=0,
            clicks=0,
        )
    )

