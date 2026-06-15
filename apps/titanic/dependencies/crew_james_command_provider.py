from sqlalchemy.ext.asyncio import AsyncSession
"""
JamesCommand 의존성 조립소 (DIP 팩토리).

DIP 원칙:
  - 라우터는 구현체(JamesPgRepository)를 직접 알지 못한다.
  - 리턴 타입은 구현체가 아닌 포트(JamesCommandUseCase)로 선언한다.
  - 세션은 core 의 get_db 에서 주입받는다 (AsyncSession).
"""
from fastapi import Depends

from core.matrix.oracle_database import get_db
from apps.titanic.adapter.outbound.pg.crew_james_pg_repository import JamesPgRepository
from apps.titanic.app.ports.input.crew_james_command_use_case import JamesCommandUseCase
from apps.titanic.app.ports.output.crew_james_repository import JamesRepository
from apps.titanic.app.use_cases.crew_james_command_interactor import JamesCommandInteractor


def get_james_command_repository(
        db: AsyncSession = Depends(get_db)
) -> JamesRepository:

    return JamesPgRepository(session=db)

def get_james_command_use_case(
        repository: JamesRepository = Depends(get_james_command_repository)
) -> JamesCommandUseCase:

    return JamesCommandInteractor(repository=repository)
