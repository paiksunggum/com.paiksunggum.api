from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any

from apps.admin.adapter.inbound.api.schemas.practice_schema import PracticeSchema
from apps.admin.app.dtos.practice_dto import PracticeResponse


class PracticeUseCase(ABC):

    @abstractmethod
    def introduce_myself(self, schema: PracticeSchema) -> PracticeResponse:
        '''practice 의 자기소개 메소드'''
        pass
