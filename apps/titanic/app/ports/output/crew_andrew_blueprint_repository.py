from abc import ABC , abstractmethod

from apps.titanic.app.dtos.crew_andrew_blueprint_dto import AndrewBlueprintQuery, AndrewBlueprintResponse

class AndrewBlueprintRepository(ABC):
    '''앤드류의 승객 명단 관리 저장소'''

    @abstractmethod
    async def introduce_myself(self, query: AndrewBlueprintQuery) -> AndrewBlueprintResponse:
        '''앤드류의 자기 소개 레포지토리 추상 메소드'''
        pass
    