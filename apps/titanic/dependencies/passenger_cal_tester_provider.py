from sqlalchemy.ext.asyncio import AsyncSession
"""
CalTester 의존성 조립소 (DIP 팩토리).

DIP 원칙:
  - 라우터는 구현체(CalTesterRepository)를 직접 알지 못한다.
  - 리턴 타입은 구현체가 아닌 포트(CalTesterUseCase)로 선언한다.
  - 세션은 core 의 get_db 에서 주입받는다 (AsyncSession).
"""
from fastapi import Depends

from core.matrix.oracle_database import get_db
from apps.titanic.adapter.outbound.repositories.passenger_cal_tester_repository import (
    CalTesterRepository,
)
from apps.titanic.app.ports.input.passenger_cal_tester_use_case import CalTesterUseCase
from apps.titanic.app.ports.output.passenger_cal_tester_port import CalTestPort
from apps.titanic.app.use_cases.passenger_cal_tester_interactor import CalTesterInteractor


def get_cal_tester_repository(
        db: AsyncSession = Depends(get_db)
) -> CalTestPort:

    return CalTesterRepository(session=db)

def get_cal_tester_use_case(
        repository: CalTestPort = Depends(get_cal_tester_repository)
) -> CalTesterUseCase:

    return CalTesterInteractor(repository=repository)
