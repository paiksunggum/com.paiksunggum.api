from __future__ import annotations

from abc import ABC, abstractmethod

from apps.silicon_valley.app.dtos.piper_coo_dto import PiperCooQuery, PiperCooResponse


class PiperCooPort(ABC):

    @abstractmethod
    async def introduce_myself(self, query: PiperCooQuery) -> PiperCooResponse:
        '''COO 포트 추상 메소드'''
        pass
