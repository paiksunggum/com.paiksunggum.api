from __future__ import annotations

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from apps.automode.adapter.outbound.repositories.juso_repository import JusoRepository
from apps.automode.app.ports.input.i_juso_use_case import IJusoUseCase
from apps.automode.app.ports.output.i_juso_port import IJusoPort
from apps.automode.app.use_cases.juso_interactor import JusoInteractor
from core.matrix.oracle_database import get_db


def get_juso_repository(
    db: AsyncSession = Depends(get_db),
) -> IJusoPort:
    return JusoRepository(session=db)


def get_juso_use_case(
    repository: IJusoPort = Depends(get_juso_repository),
) -> IJusoUseCase:
    return JusoInteractor(repository=repository)
