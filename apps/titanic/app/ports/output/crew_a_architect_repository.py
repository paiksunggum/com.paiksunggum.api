from __future__ import annotations

from abc import ABC, abstractmethod

from apps.titanic.app.dtos.crew_a_architect_dto import AArchitectQuery, AArchitectResponse


class AArchitectRepository(ABC):
    
    @abstractmethod
    async def introduce_myself(self, query: AArchitectQuery) -> AArchitectResponse:
        '''토마스 에이 아키텍트의 자기 소개 레포지토리 추상 메소드'''
        pass






    
