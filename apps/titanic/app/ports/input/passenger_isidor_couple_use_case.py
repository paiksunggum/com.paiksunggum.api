from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any

from apps.titanic.adapter.inbound.api.schemas.passenger_isidor_couple_schema import IsidorCoupleSchema
from apps.titanic.app.dtos.passenger_isidor_couple_dto import IsidorCoupleResponse


class IsidorCoupleUseCase(ABC):

    @abstractmethod
    async def introduce_myself(self, schema: IsidorCoupleSchema) -> IsidorCoupleResponse:
        '''이시도어 커플의 자기소개 메소드'''
        pass