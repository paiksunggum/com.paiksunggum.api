from sqlalchemy.ext.asyncio import AsyncSession
"""
AndrewBlueprint 의존성 조립소 (DIP 팩토리).

DIP 원칙:
  - 라우터는 구현체(AndrewBlueprintPgRepository)를 직접 알지 못한다.
  - 리턴 타입은 구현체가 아닌 포트(AndrewBlueprintUseCase)로 선언한다.
  - 세션은 core 의 get_db 에서 주입받는다 (AsyncSession).
"""
from fastapi import Depends

from core.matrix.oracle_database import get_db
from apps.titanic.adapter.outbound.pg.crew_andrew_blueprint_pg_repository import (
    AndrewBlueprintPgRepository,
)
from apps.titanic.app.ports.input.crew_andrew_blueprint_use_case import AndrewBlueprintUseCase
from apps.titanic.app.ports.output.crew_andrew_blueprint_repository import AndrewBlueprintRepository
from apps.titanic.app.use_cases.crew_andrew_blueprint_interactor import AndrewBlueprintInteractor


def get_andrew_blueprint_repository(
        db: AsyncSession = Depends(get_db)
) -> AndrewBlueprintRepository:

    return AndrewBlueprintPgRepository(session=db)

def get_andrew_blueprint_use_case(
        repository: AndrewBlueprintRepository = Depends(get_andrew_blueprint_repository)
) -> AndrewBlueprintUseCase:

    return AndrewBlueprintInteractor(repository=repository)
