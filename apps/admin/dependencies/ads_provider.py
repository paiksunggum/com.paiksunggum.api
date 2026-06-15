from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from core.matrix.oracle_database import get_db
from apps.admin.adapter.outbound.pg.ads_pg_repository import AdsPgRepository
from apps.admin.app.ports.input.ads_use_case import AdsUseCase
from apps.admin.app.ports.output.ads_repository import AdsRepository
from apps.admin.app.use_cases.ads_interactor import AdsInteractor


def get_ads_use_case(
        db: AsyncSession = Depends(get_db),
) -> AdsUseCase:
    repository: AdsRepository = AdsPgRepository(session=db)
    return AdsInteractor(repository=repository)
