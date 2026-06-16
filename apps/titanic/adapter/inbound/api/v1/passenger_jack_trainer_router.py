import logging

from fastapi import APIRouter, Depends
from apps.titanic.adapter.inbound.api.schemas.passenger_jack_trainer_schema import (
    JackTrainerResponseSchema,
    JackTrainerSchema,
)
from apps.titanic.app.ports.input.passenger_jack_trainer_use_case import JackTrainerUseCase
from apps.titanic.dependencies.passenger_jack_trainer_provider import get_jack_trainer_use_case

'''
잭 도슨 (Jack Dawson)
자유로운 영혼, 예술가, 그리고 로즈를 구원하는 인물인 만큼
'그림'이나 '포커 도박'과 관련된 키워드가 잘 어울립니다.
생존 예측 모델의 핵심 인터페이스를 담당합니다.
'''
logger = logging.getLogger("apps")
jack_trainer_router = APIRouter(prefix="/jack", tags=["jack"])


@jack_trainer_router.get("/myself", response_model=JackTrainerResponseSchema)
async def introduce_myself(
    jack: JackTrainerUseCase = Depends(get_jack_trainer_use_case),
) -> JackTrainerResponseSchema:
    result = await jack.introduce_myself(
        JackTrainerSchema(
            id=9,
            name="Jack Dawson",
        )
    )
    return JackTrainerResponseSchema(id=result.id, name=result.name)


@jack_trainer_router.get("/train")
async def get_model_train(
    jack: JackTrainerUseCase = Depends(get_jack_trainer_use_case),
) -> dict:
    return await jack.train_model(None)
