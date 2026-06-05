from datetime import date

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..models.ad_stats_daily_model import AdStatsDaily


class AdStatsDailyRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create(self, row: AdStatsDaily) -> AdStatsDaily:
        self.session.add(row)
        await self.session.commit()
        await self.session.refresh(row)
        return row

    async def list_by_ad_id(
        self,
        ad_id: int,
        from_date: date | None = None,
        to_date: date | None = None,
    ) -> list[AdStatsDaily]:
        stmt = select(AdStatsDaily).where(AdStatsDaily.ad_id == ad_id)
        if from_date is not None:
            stmt = stmt.where(AdStatsDaily.stat_date >= from_date)
        if to_date is not None:
            stmt = stmt.where(AdStatsDaily.stat_date <= to_date)
        stmt = stmt.order_by(AdStatsDaily.stat_date.desc())
        result = await self.session.execute(stmt)
        return list(result.scalars().all())
