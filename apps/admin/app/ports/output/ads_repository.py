from __future__ import annotations

from abc import ABC, abstractmethod

from apps.admin.app.dtos.ads_dto import AdsQuery, AdsResponse


class AdsRepository(ABC):

    @abstractmethod
    def introduce_myself(self, query: AdsQuery) -> AdsResponse:
        '''ads 의 자기 소개 레포지토리 추상 메소드'''
        pass
