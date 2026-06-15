from __future__ import annotations

from abc import ABC, abstractmethod

from apps.admin.app.dtos.sports_dto import SportsQuery, SportsResponse


class SportsRepository(ABC):

    @abstractmethod
    def introduce_myself(self, query: SportsQuery) -> SportsResponse:
        '''sports 의 자기 소개 레포지토리 추상 메소드'''
        pass
