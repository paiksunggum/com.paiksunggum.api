from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from core.matrix.oracle_database import get_db
from apps.admin.adapter.outbound.pg.practice_pg_repository import PracticePgRepository
from apps.admin.app.ports.input.practice_use_case import PracticeUseCase
from apps.admin.app.ports.output.practice_repository import PracticeRepository
from apps.admin.app.use_cases.practice_interactor import PracticeInteractor


def get_practice_use_case(
        db: AsyncSession = Depends(get_db),
) -> PracticeUseCase:
    repository: PracticeRepository = PracticePgRepository(session=db)
    return PracticeInteractor(repository=repository)
