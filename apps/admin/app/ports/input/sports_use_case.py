from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any

from apps.admin.adapter.inbound.api.schemas.sports_schema import SportsSchema
from apps.admin.app.dtos.sports_dto import SportsResponse


class SportsUseCase(ABC):

    @abstractmethod
    def introduce_myself(self, schema: SportsSchema) -> SportsResponse:
        '''sports 의 자기소개 메소드'''
        pass
