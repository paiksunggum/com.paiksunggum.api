from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any

from apps.admin.adapter.inbound.api.schemas.ads_schema import AdsSchema
from apps.admin.app.dtos.ads_dto import AdsResponse


class AdsUseCase(ABC):

    @abstractmethod
    def introduce_myself(self, schema: AdsSchema) -> AdsResponse:
        '''ads 의 자기소개 메소드'''
        pass
