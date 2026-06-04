from abc import ABC, abstractmethod

from apps.titanic.app.dtos.andrew_blueprint_dto import AndrewBlueprintQuery


class AndrewBlueprintRepository(ABC):

    @abstractmethod
    def introduce_myself(self, query: AndrewBlueprintQuery):
        '''앤드류의 자기소개 메소드'''
        pass
