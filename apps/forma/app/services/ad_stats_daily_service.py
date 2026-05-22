from datetime import date

from sqlalchemy.ext.asyncio import AsyncSession

from ..models.ad_stats_daily_model import AdStatsDaily
from ..repositories.ad_stats_daily_repository import AdStatsDailyRepository
from ..schemas.ad_stats_daily_schema import AdStatsDailyNestedCreateRequest


class AdStatsDailyService:
    def __init__(self, session: AsyncSession) -> None:
        self.repository = AdStatsDailyRepository(session)

    async def create_for_ad(
        self, ad_id: int, req: AdStatsDailyNestedCreateRequest
    ) -> AdStatsDaily:
        row = AdStatsDaily(
            ad_id=ad_id,
            stat_date=req.stat_date,
            impressions=req.impressions,
            clicks=req.clicks,
        )
        return await self.repository.create(row)

    async def list_for_ad(
        self,
        ad_id: int,
        from_date: date | None = None,
        to_date: date | None = None,
    ) -> list[AdStatsDaily]:
        return await self.repository.list_by_ad_id(ad_id, from_date, to_date)
