from __future__ import annotations

from abc import ABC, abstractmethod

from apps.silicon_valley.app.dtos.piper_ceo_dto import PiperCeoQuery, PiperCeoResponse


class PiperCeoPort(ABC):

    @abstractmethod
    async def introduce_myself(self, query: PiperCeoQuery) -> PiperCeoResponse:
        '''CEO 포트 추상 메소드'''
        pass
