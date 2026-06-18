from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any

from apps.titanic.adapter.inbound.api.schemas.crew_lowe_boat_schema import LoweBoatSchema
from apps.titanic.app.dtos.crew_lowe_boat_dto import LoweBoatQuery, LoweBoatResponse

class LoweBoatUseCase(ABC):

    @abstractmethod
    def feature_engineering(self, train_set, test_set=None):
        pass

    @abstractmethod
    async def introduce_myself(self, schema: LoweBoatSchema) -> LoweBoatResponse:
        '''로우 보우트의 자기소개 메소드'''
        pass