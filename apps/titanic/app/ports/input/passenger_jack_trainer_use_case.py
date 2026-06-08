from __future__ import annotations

from abc import ABC, abstractmethod

from apps.titanic.app.dtos.passenger_jack_trainer_dto import JackTrainerResponse


class JackTrainerUseCase(ABC):

    @abstractmethod
    async def introduce_myself(self, schema: JackTrainerSchema) -> JackTrainerResponse:
        '''잭 도슨의 자기소개 메소드'''
        pass
