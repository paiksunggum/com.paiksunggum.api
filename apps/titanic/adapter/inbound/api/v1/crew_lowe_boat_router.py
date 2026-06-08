import logging

from fastapi import APIRouter, Depends
from apps.titanic.adapter.inbound.api.schemas.crew_lowe_boat_chema import (
    LoweBoatResponseSchema,
    LoweBoatSchema,
)
from apps.titanic.app.ports.input.crew_lowe_boat_use_case import LoweBoatUseCase
from apps.titanic.dependencies.crew_lowe_boat_provider import get_lowe_boat_use_case

'''
해롤드 로우 (Harold Lowe)
자유로운 영혼, 예술가, 그리고 로즈를 구원하는 인물인 만큼
'그림'이나 '포커 도박'과 관련된 키워드가 잘 어울립니다.
생존 예측 모델의 핵심 인터페이스를 담당합니다.
'''
logger = logging.getLogger("apps")
lowe_boat_router = APIRouter(prefix="/lowe", tags=["lowe"])


@lowe_boat_router.get("/myself", response_model=LoweBoatResponseSchema)
async def introduce_myself(
    lowe: LoweBoatUseCase = Depends(get_lowe_boat_use_case),
) -> LoweBoatResponseSchema:
    result = await lowe.introduce_myself(
        LoweBoatSchema(
            id=4,
            name="Harold Lowe",
        )
    )
    return LoweBoatResponseSchema(id=result.id, name=result.name)
