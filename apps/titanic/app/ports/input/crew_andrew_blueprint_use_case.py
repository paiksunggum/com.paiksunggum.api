from abc import ABC, abstractmethod

from apps.titanic.adapter.inbound.api.schemas.crew_andrew_blueprint_schema import AndrewBlueprintSchema
from apps.titanic.app.dtos.crew_andrew_blueprint_dto import AndrewBlueprintResponse


class AndrewBlueprintUseCase(ABC):
    @abstractmethod
    async def introduce_myself(self,
        schema: AndrewBlueprintSchema,
    ) -> AndrewBlueprintResponse:
        pass

    @abstractmethod
    async def get_train_set(self) -> AndrewBlueprintResponse:
        '''앤드류가 DB에서 train set 만 가져오는 메소드'''
        pass

    @abstractmethod
    async def get_test_set(self) -> AndrewBlueprintResponse:
        '''앤드류의 자기소개 메소드'''
        pass