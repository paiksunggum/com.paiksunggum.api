import logging

from fastapi import APIRouter, Depends
from apps.titanic.adapter.inbound.api.schemas.passenger_rose_model_schema import (
    RoseModelResponseSchema,
    RoseModelSchema,
)
from apps.titanic.app.ports.input.passenger_rose_model_use_case import RoseModelUseCase
from apps.titanic.dependencies.passenger_rose_model_provider import get_rose_model_use_case

'''
로즈 드윗 부카터 (Rose DeWitt Bukater)
상류층의 답답함에서 벗어나고자 하는 의지, 그리고
영화의 핵심 매개체인 '다이아몬드'와 관련된 키워드입니다.
'''
logger = logging.getLogger("apps")
rose_model_router = APIRouter(prefix="/rose", tags=["rose"])


@rose_model_router.get("/myself", response_model=RoseModelResponseSchema)
async def introduce_myself(
    rose: RoseModelUseCase = Depends(get_rose_model_use_case),
) -> RoseModelResponseSchema:
    result = await rose.introduce_myself(
        RoseModelSchema(
            id=11,
            name="Rose DeWitt Bukater",
        )
    )
    return RoseModelResponseSchema(id=result.id, name=result.name)