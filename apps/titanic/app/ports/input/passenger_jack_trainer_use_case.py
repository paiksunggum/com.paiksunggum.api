from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any

from apps.titanic.adapter.inbound.api.schemas.passenger_jack_trainer_schema import JackTrainerSchema
from apps.titanic.app.dtos.passenger_jack_trainer_dto import JackTrainerResponse


class JackTrainerUseCase(ABC):

    @abstractmethod
    async def introduce_myself(self, schema: JackTrainerSchema) -> JackTrainerResponse:
        '''잭 도슨의 자기소개 메소드'''
        pass

    @abstractmethod
    def train_model(self, train_set) -> JackTrainerResponse:
        '''로즈가 제안한 모델들을 훈련시키는 메소드'''
        pass
