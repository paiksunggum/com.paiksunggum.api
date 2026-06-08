from __future__ import annotations

from abc import ABC, abstractmethod

from apps.titanic.app.dtos.passenger_molly_scaler_dto import MollyScalerResponse


class MollyScalerUseCase(ABC):

    @abstractmethod
    async def introduce_myself(self, schema: MollyScalerSchema) -> MollyScalerResponse:
        '''몰리 브라운의 자기소개 메소드'''
        pass
