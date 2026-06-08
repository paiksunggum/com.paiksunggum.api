from __future__ import annotations

from abc import ABC, abstractmethod

from apps.titanic.app.dtos.passenger_ruth_validation_dto import RuthValidationResponse


class RuthValidationUseCase(ABC):

    @abstractmethod
    async def introduce_myself(self, schema: RuthValidationSchema) -> RuthValidationResponse:
        '''루쓰 드윗 부카터의 자기소개 메소드'''
        pass
