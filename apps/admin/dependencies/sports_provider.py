from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from core.matrix.oracle_database import get_db
from apps.admin.adapter.outbound.pg.sports_pg_repository import SportsPgRepository
from apps.admin.app.ports.input.sports_use_case import SportsUseCase
from apps.admin.app.ports.output.sports_repository import SportsRepository
from apps.admin.app.use_cases.sports_interactor import SportsInteractor


def get_sports_use_case(
        db: AsyncSession = Depends(get_db),
) -> SportsUseCase:
    repository: SportsRepository = SportsPgRepository(session=db)
    return SportsInteractor(repository=repository)
