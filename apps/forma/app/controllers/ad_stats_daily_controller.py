from datetime import date

from sqlalchemy.ext.asyncio import AsyncSession

from ..schemas.ad_stats_daily_schema import AdStatsDailyNestedCreateRequest
from ..services.ad_stats_daily_service import AdStatsDailyService


class AdStatsDailyController:
    def __init__(self, session: AsyncSession) -> None:
        self.service = AdStatsDailyService(session)

    async def create_for_ad(self, ad_id: int, req: AdStatsDailyNestedCreateRequest):
        return await self.service.create_for_ad(ad_id, req)

    async def list_for_ad(
        self,
        ad_id: int,
        from_date: date | None = None,
        to_date: date | None = None,
    ):
        return await self.service.list_for_ad(ad_id, from_date, to_date)
