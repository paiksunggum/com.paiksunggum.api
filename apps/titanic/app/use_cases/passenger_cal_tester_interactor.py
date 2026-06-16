from __future__ import annotations
import logging
from typing import Any

from apps.titanic.adapter.inbound.api.schemas.passenger_cal_tester_schema import CalTesterSchema
from apps.titanic.app.dtos.passenger_cal_tester_dto import CalTesterQuery, CalTesterResponse
from apps.titanic.app.ports.input.passenger_cal_tester_use_case import CalTesterUseCase
from apps.titanic.app.ports.output.passenger_cal_tester_repository import CalTestRepository

logger = logging.getLogger("apps")


class CalTesterInteractor(CalTesterUseCase):

    def __init__(self, repository: CalTestRepository):
        self.repository = repository

    async def test_model(self, test_set) -> CalTesterResponse:
        '''칼이 로즈가 제안한 10개 모델의 트레이닝 정도를 점수화 해서 1등을 뽑는 것'''
        best_name, best_metrics = max(
            test_set.items(),
            key=lambda x: x[1]["accuracy"],
        )
        result = {"rank": 1, "algorithm": best_name, **best_metrics}
        logger.info("CalTesterInteractor: best_model=%s", result)
        return result

    async def introduce_myself(self, schema: CalTesterSchema) -> CalTesterResponse:
        '''칼 헉클리의 자기소개 인터렉트'''
        return await self.repository.introduce_myself(CalTesterQuery(
            id=schema.id,
            name=schema.name,
        ))
