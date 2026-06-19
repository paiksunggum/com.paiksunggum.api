from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends

from core.matrix.oracle_database import get_db
from apps.silicon_valley.adapter.outbound.repositories.piper_dash_repository import PiperDashRepository
from apps.silicon_valley.app.ports.input.piper_dash_use_case import PiperDashUseCase
from apps.silicon_valley.app.ports.output.piper_dash_port import PiperDashPort
from apps.silicon_valley.app.use_cases.piper_dash_interactor import PiperDashInteractor


def get_piper_dash_repository(
    db: AsyncSession = Depends(get_db),
) -> PiperDashPort:
    return PiperDashRepository(session=db)


def get_piper_dash_use_case(
    repository: PiperDashPort = Depends(get_piper_dash_repository),
) -> PiperDashUseCase:
    return PiperDashInteractor(repository=repository)
