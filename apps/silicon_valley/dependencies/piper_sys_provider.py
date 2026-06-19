from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends

from core.matrix.oracle_database import get_db
from apps.silicon_valley.adapter.outbound.repositories.piper_sys_repository import PiperSysRepository
from apps.silicon_valley.app.ports.input.piper_sys_use_case import PiperSysUseCase
from apps.silicon_valley.app.ports.output.piper_sys_port import PiperSysPort
from apps.silicon_valley.app.use_cases.piper_sys_interactor import PiperSysInteractor


def get_piper_sys_repository(
    db: AsyncSession = Depends(get_db),
) -> PiperSysPort:
    return PiperSysRepository(session=db)


def get_piper_sys_use_case(
    repository: PiperSysPort = Depends(get_piper_sys_repository),
) -> PiperSysUseCase:
    return PiperSysInteractor(repository=repository)
