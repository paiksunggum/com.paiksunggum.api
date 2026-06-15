from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from core.matrix.oracle_database import get_db
from apps.admin.adapter.outbound.pg.ad_stats_daily_pg_repository import AdStatsDailyPgRepository
from apps.admin.app.ports.input.ad_stats_daily_use_case import AdStatsDailyUseCase
from apps.admin.app.ports.output.ad_stats_daily_repository import AdStatsDailyRepository
from apps.admin.app.use_cases.ad_stats_daily_interactor import AdStatsDailyInteractor


def get_ad_stats_daily_use_case(
        db: AsyncSession = Depends(get_db),
) -> AdStatsDailyUseCase:
    repository: AdStatsDailyRepository = AdStatsDailyPgRepository(session=db)
    return AdStatsDailyInteractor(repository=repository)