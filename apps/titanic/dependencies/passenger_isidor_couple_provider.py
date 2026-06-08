from sqlalchemy.ext.asyncio import AsyncSession
"""
IsidorCouple 의존성 조립소 (DIP 팩토리).

DIP 원칙:
  - 라우터는 구현체(IsidorCouplePgRepository)를 직접 알지 못한다.
  - 리턴 타입은 구현체가 아닌 포트(IsidorCoupleUseCase)로 선언한다.
  - 세션은 core 의 get_db 에서 주입받는다 (AsyncSession).
"""
from fastapi import Depends

from core.matrix.oracle_database import get_db
from apps.titanic.adapter.outbound.pg.passenger_isidor_couple_pg_repository import (
    IsidorCouplePgRepository,
)
from apps.titanic.app.ports.input.passenger_isidor_couple_use_case import IsidorCoupleUseCase
from apps.titanic.app.ports.output.passenger_isidor_couple_repository import IsidorCoupleRepository
from apps.titanic.app.use_cases.passenger_isidor_couple_interactor import IsidorCoupleInteractor


def get_isidor_couple_use_case(
    db: AsyncSession = Depends(get_db),
) -> IsidorCoupleUseCase:
    repository: IsidorCoupleRepository = IsidorCouplePgRepository(session=db)
    return IsidorCoupleInteractor(repository=repository)
