from __future__ import annotations

from abc import ABC, abstractmethod

from apps.admin.app.dtos.ad_stats_daily_dto import AdStatsDailyQuery, AdStatsDailyResponse


class AdStatsDailyRepository(ABC):

    @abstractmethod
    def introduce_myself(self, query: AdStatsDailyQuery) -> AdStatsDailyResponse:
        '''ad_stats_daily 의 자기 소개 레포지토리 추상 메소드'''
        pass