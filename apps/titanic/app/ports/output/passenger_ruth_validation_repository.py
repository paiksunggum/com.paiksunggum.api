from __future__ import annotations

from abc import ABC, abstractmethod
from apps.titanic.app.dtos.passenger_ruth_validation_dto import RuthValidationQuery, RuthValidationResponse


class RuthValidationRepository(ABC):

    @abstractmethod
    async def introduce_myself(
        query: RuthValidationQuery,
    ) -> RuthValidationResponse:
        '''루쓰 드윗 부카터의 자기 소개 레포지토리 추상 메소드'''
        pass