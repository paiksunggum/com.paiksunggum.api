from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any

from apps.admin.adapter.inbound.api.schemas.ad_stats_daily_schema import AdStatsDailySchema
from apps.admin.app.dtos.ad_stats_daily_dto import AdStatsDailyResponse


class AdStatsDailyUseCase(ABC):

    @abstractmethod
    def introduce_myself(self, schema: AdStatsDailySchema) -> AdStatsDailyResponse:
        '''ad_stats_daily 의 자기소개 메소드'''
        pass