from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any

from apps.titanic.adapter.inbound.api.schemas.crew_a_architect_schema import AArchitectSchema
from apps.titanic.app.dtos.crew_a_architect_dto import AArchitectResponse


class AArchitectUseCase(ABC):

    @abstractmethod
    async def introduce_myself(self, schema: AArchitectSchema) -> AArchitectResponse:
        '''토마스 에이 아키텍트의 자기소개 메소드'''
        pass

    @abstractmethod
    def analyze_intent(self, question: str) -> dict[str, Any]:
        '''Kiwi 형태소 분석으로 프론트 질문의 의도를 파악하는 추상 메소드'''
        pass





