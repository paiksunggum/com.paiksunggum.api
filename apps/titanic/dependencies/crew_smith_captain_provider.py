from sqlalchemy.ext.asyncio import AsyncSession
"""
SmithCaptain 의존성 조립소 (DIP 팩토리).

DIP 원칙:
  - 라우터는 구현체(SmithCaptainPgRepository)를 직접 알지 못한다.
  - 리턴 타입은 구현체가 아닌 포트(SmithCaptainUseCase)로 선언한다.
  - 세션은 core 의 get_db 에서 주입받는다 (AsyncSession).
"""
from fastapi import Depends

from core.matrix.oracle_database import get_db
from apps.titanic.adapter.outbound.pg.crew_smith_captain_pg_repository import (
    SmithCaptainPgRepository,
)
from apps.titanic.app.ports.input.crew_smith_captain_use_case import SmithCaptainUseCase
from apps.titanic.app.ports.output.crew_smith_captain_repository import SmithCaptainRepository
from apps.titanic.app.use_cases.crew_smith_captain_interactor import SmithCaptainInteractor
from apps.titanic.app.ports.input.passenger_jack_trainer_use_case import JackTrainerUseCase
from apps.titanic.app.ports.input.passenger_rose_model_use_case import RoseModelUseCase
from apps.titanic.app.ports.input.passenger_cal_tester_use_case import CalTesterUseCase
from apps.titanic.app.ports.input.crew_andrew_blueprint_use_case import AndrewBlueprintUseCase
from apps.titanic.dependencies.passenger_jack_trainer_provider import get_jack_trainer_use_case
from apps.titanic.dependencies.passenger_rose_model_provider import get_rose_model_use_case
from apps.titanic.dependencies.passenger_cal_tester_provider import get_cal_tester_use_case
from apps.titanic.dependencies.crew_andrew_blueprint_provider import get_andrew_blueprint_use_case


def get_smith_captain_repository(
        db: AsyncSession = Depends(get_db)
) -> SmithCaptainRepository:

    return SmithCaptainPgRepository(session=db)

def get_smith_captain_use_case(
        repository: SmithCaptainRepository = Depends(get_smith_captain_repository),
        jack: JackTrainerUseCase = Depends(get_jack_trainer_use_case),
        rose: RoseModelUseCase = Depends(get_rose_model_use_case),
        cal: CalTesterUseCase = Depends(get_cal_tester_use_case),
        andrew: AndrewBlueprintUseCase = Depends(get_andrew_blueprint_use_case),
) -> SmithCaptainUseCase:

    return SmithCaptainInteractor(
        repository=repository,
        jack=jack,
        rose=rose,
        cal=cal,
        andrew=andrew,
    )
