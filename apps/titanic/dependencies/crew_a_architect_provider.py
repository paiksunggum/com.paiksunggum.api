from sqlalchemy.ext.asyncio import AsyncSession
"""
AArchitect 의존성 조립소 (DIP 팩토리).

DIP 원칙:
  - 라우터는 구현체(AArchitectPgRepository)를 직접 알지 못한다.
  - 리턴 타입은 구현체가 아닌 포트(AArchitectUseCase)로 선언한다.
  - 세션은 core 의 get_db 에서 주입받는다 (AsyncSession).
"""
from fastapi import Depends

from core.matrix.oracle_database import get_db
from apps.titanic.adapter.outbound.pg.crew_a_architect_pg_repository import (
    AArchitectPgRepository,
)
from apps.titanic.app.ports.input.crew_a_architect_use_case import AArchitectUseCase
from apps.titanic.app.ports.output.crew_a_architect_repository import AArchitectRepository
from apps.titanic.app.use_cases.crew_a_architect_interactor import AArchitectInteractor


def get_a_architect_use_case(
    db: AsyncSession = Depends(get_db),
) -> AArchitectUseCase:
    repository: AArchitectRepository = AArchitectPgRepository(session=db)
    return AArchitectInteractor(repository=repository)
