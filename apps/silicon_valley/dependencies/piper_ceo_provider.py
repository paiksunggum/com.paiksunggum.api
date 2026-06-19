from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends

from core.matrix.oracle_database import get_db
from apps.silicon_valley.adapter.outbound.repositories.piper_ceo_repository import PiperCeoRepository
from apps.silicon_valley.app.ports.input.piper_ceo_use_case import PiperCeoUseCase
from apps.silicon_valley.app.ports.output.piper_ceo_port import PiperCeoPort
from apps.silicon_valley.app.use_cases.piper_ceo_interactor import PiperCeoInteractor


def get_piper_ceo_repository(
    db: AsyncSession = Depends(get_db),
) -> PiperCeoPort:
    return PiperCeoRepository(session=db)


def get_piper_ceo_use_case(
    repository: PiperCeoPort = Depends(get_piper_ceo_repository),
) -> PiperCeoUseCase:
    return PiperCeoInteractor(repository=repository)
