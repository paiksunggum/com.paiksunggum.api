import logging

from fastapi import APIRouter, Depends
from apps.titanic.adapter.inbound.api.schemas.crew_andrew_blueprint_schema import (
    AndrewBlueprintResponseSchema,
    AndrewBlueprintSchema,
)
from apps.titanic.app.ports.input.crew_andrew_blueprint_use_case import AndrewBlueprintUseCase
from apps.titanic.dependencies.crew_andrew_blueprint_provider import get_andrew_blueprint_use_case

'''
영화 <타이타닉>에서 승객 명단을 관리하는
일등 항해사 윌터 와일딩(Andrew / 혹은 윌리엄 머독 등 영화 속 관리자 캐릭터)
또는 승객 명단(Passenger List)을 다루는 '월터'라는 인물의 상황에 맞추어,
직관적이면서도 센스 있는 중간 키워드를 추천해 드립니다.
'''
logger = logging.getLogger("apps")
andrew_blueprint_router = APIRouter(prefix="/andrew", tags=["andrew"])


@andrew_blueprint_router.get("/myself", response_model=AndrewBlueprintResponseSchema)
async def introduce_myself(
    andrew: AndrewBlueprintUseCase = Depends(get_andrew_blueprint_use_case),
) -> AndrewBlueprintResponseSchema:
    result = await andrew.introduce_myself(
        AndrewBlueprintSchema(
            id=6,
            name="Andrew Blueprint",
            memo="타이타닉의 일등 항해사, 승객 명단 관리 담당",
        )
    )
    return AndrewBlueprintResponseSchema(
        id=result.id,
        name=result.name,
        memo=result.memo,
    )
