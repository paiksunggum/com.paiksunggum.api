from __future__ import annotations

from abc import ABC, abstractmethod

from apps.silicon_valley.app.dtos.piper_sys_dto import PiperSysQuery, PiperSysResponse


class PiperSysPort(ABC):

    @abstractmethod
    async def introduce_myself(self, query: PiperSysQuery) -> PiperSysResponse:
        '''Systems Architect 포트 추상 메소드'''
        pass
