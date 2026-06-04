from abc import ABC, abstractmethod

from apps.titanic.adapter.inbound.api.schemas.andrew_blueprint_schema import AndrewBlueprintSchema


class AndrewBlueprintUseCase(ABC):

    @abstractmethod
    def introduce_myself(self, schema: AndrewBlueprintSchema):
        '''앤드류의 자기소개 메소드'''
        pass
