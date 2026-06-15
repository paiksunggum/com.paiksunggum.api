from __future__ import annotations

from abc import ABC, abstractmethod

from apps.admin.app.dtos.practice_dto import PracticeQuery, PracticeResponse


class PracticeRepository(ABC):

    @abstractmethod
    def introduce_myself(self, query: PracticeQuery) -> PracticeResponse:
        '''practice 의 자기 소개 레포지토리 추상 메소드'''
        pass
