from __future__ import annotations

from abc import ABC, abstractmethod

import pandas as pd

from apps.titanic.adapter.inbound.api.schemas.crew_hartley_violin_schema import HartleyViolinSchema
from apps.titanic.app.dtos.crew_hartley_violin_dto import HartleyViolinResponse


class HartleyViolinUseCase(ABC):

    @abstractmethod
    async def introduce_myself(self, schema: HartleyViolinSchema) -> HartleyViolinResponse:
        '''하틀리 바이올린의 자기소개 메소드'''
        pass

    @abstractmethod
    def get_correlation_plot(self, df: pd.DataFrame) -> bytes:
        '''피처 상관관계 히트맵을 PNG 바이트로 반환'''
        pass