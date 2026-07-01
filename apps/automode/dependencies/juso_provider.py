from __future__ import annotations

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from apps.automode.adapter.outbound.repositories.juso_repository import JusoRepository
from apps.automode.app.ports.input.juso_use_case import JusoUseCase
from apps.automode.app.ports.output.juso_port import JusoPort
from apps.automode.app.use_cases.juso_interactor import JusoInteractor
from core.matrix.oracle_database import get_db


def get_juso_repository(
    db: AsyncSession = Depends(get_db),
) -> JusoPort:
    return JusoRepository(session=db)


def get_juso_use_case(
    repository: JusoPort = Depends(get_juso_repository),
) -> JusoUseCase:
    return JusoInteractor(repository=repository)
