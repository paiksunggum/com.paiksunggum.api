from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any

from apps.titanic.adapter.inbound.api.schemas.passenger_cal_tester_schema import CalTesterSchema
from apps.titanic.app.dtos.passenger_cal_tester_dto import CalTesterResponse


class CalTesterUseCase(ABC):

    @abstractmethod
    async def introduce_myself(self, schema: CalTesterSchema) -> CalTesterResponse:
        '''칼 테스터의 자기소개 메소드'''
        pass

    @abstractmethod
    def test_model(self, test_set) -> CalTesterResponse:
        '''잭이 훈련한 모델들을 정확도 기준으로 순위를 매기는 메소드'''
        pass