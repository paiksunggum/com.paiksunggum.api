from __future__ import annotations

from abc import ABC, abstractmethod

from apps.silicon_valley.app.dtos.piper_dash_dto import PiperDashQuery, PiperDashResponse


class PiperDashPort(ABC):

    @abstractmethod
    async def introduce_myself(self, query: PiperDashQuery) -> PiperDashResponse:
        '''Dashboard 포트 추상 메소드'''
        pass
