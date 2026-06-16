import logging

from fastapi import APIRouter, Depends
from apps.titanic.adapter.inbound.api.schemas.passenger_cal_tester_schema import (
    CalTesterResponseSchema,
    CalTesterSchema,
)
from apps.titanic.app.ports.input.passenger_cal_tester_use_case import CalTesterUseCase
from apps.titanic.app.ports.input.passenger_jack_trainer_use_case import JackTrainerUseCase
from apps.titanic.dependencies.passenger_cal_tester_provider import get_cal_tester_use_case
from apps.titanic.dependencies.passenger_jack_trainer_provider import get_jack_trainer_use_case

'''
칼 캘던 하클리 (Caledon Hockley)
오만하고 부유한 자산가이자, 소유욕이 강하고 빌런으로서의
면모를 드러내는 키워드입니다.
승객 입력값 유효성 검사를 담당합니다.
'''
logger = logging.getLogger("apps")
cal_tester_router = APIRouter(prefix="/cal", tags=["cal"])


@cal_tester_router.get("/myself", response_model=CalTesterResponseSchema)
async def introduce_myself(
    cal: CalTesterUseCase = Depends(get_cal_tester_use_case),
) -> CalTesterResponseSchema:
    result = await cal.introduce_myself(
        CalTesterSchema(
            id=7,
            name="Caledon Hockley",
        )
    )
    return CalTesterResponseSchema(id=result.id, name=result.name)


@cal_tester_router.get("/rank")
async def get_model_rank(
    jack: JackTrainerUseCase = Depends(get_jack_trainer_use_case),
    cal: CalTesterUseCase = Depends(get_cal_tester_use_case),
) -> dict:
    train_results = await jack.train_model(None)
    return await cal.test_model(train_results)
