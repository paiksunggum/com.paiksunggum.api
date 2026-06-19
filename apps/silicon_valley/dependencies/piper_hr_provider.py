from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends

from core.matrix.oracle_database import get_db
from apps.silicon_valley.adapter.outbound.repositories.piper_hr_repository import PiperHrRepository
from apps.silicon_valley.app.ports.input.piper_hr_use_case import PiperHrUseCase
from apps.silicon_valley.app.ports.output.piper_hr_port import PiperHrPort
from apps.silicon_valley.app.use_cases.piper_hr_interactor import PiperHrInteractor


def get_piper_hr_repository(
    db: AsyncSession = Depends(get_db),
) -> PiperHrPort:
    return PiperHrRepository(session=db)


def get_piper_hr_use_case(
    repository: PiperHrPort = Depends(get_piper_hr_repository),
) -> PiperHrUseCase:
    return PiperHrInteractor(repository=repository)
