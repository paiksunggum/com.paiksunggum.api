import logging

from fastapi import APIRouter, Depends

from apps.titanic.adapter.inbound.api.schemas.crew_a_architect_schema import (
    AArchitectResponseSchema,
    AArchitectSchema,
)
from apps.titanic.app.ports.input.crew_a_architect_use_case import AArchitectUseCase
from apps.titanic.dependencies.crew_a_architect_provider import get_a_architect_use_case
from apps.titanic.app.dtos.crew_a_architect_dto import AArchitectQuery, AArchitectResponse

'''
토마스 에이 (Thomas A)
타이타닉을 설계한 수석 디자이너입니다. 배의 침몰을 가장 먼저 직감하고, 마지막 순간 흡연실 시계 앞에서 죄책감에 잠겨 있던 모습이 관객들에게 깊은 여운을 남겼습니다. 시스템의 구조나 메타데이터를 다루는 역할로 좋습니다.

추천 파일명: a_architect_router.py (Architect: 타이타닉 설계자)
'''
logger = logging.getLogger("apps")
a_architect_router = APIRouter(prefix="/a", tags=["a"])


@a_architect_router.get("/myself", response_model=AArchitectResponseSchema)
async def introduce_myself(
    a: AArchitectUseCase = Depends(get_a_architect_use_case),
) -> AArchitectResponseSchema:

    return await a.introduce_myself(
        AArchitectSchema(
            id=2,
            name="Thomas A")
    )


\