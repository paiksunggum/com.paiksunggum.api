from __future__ import annotations

from abc import ABC, abstractmethod

from apps.silicon_valley.app.dtos.piper_hr_dto import PiperHrQuery, PiperHrResponse


class PiperHrPort(ABC):

    @abstractmethod
    async def introduce_myself(self, query: PiperHrQuery) -> PiperHrResponse:
        '''HR 포트 추상 메소드'''
        pass
