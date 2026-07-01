from __future__ import annotations

from abc import ABC, abstractmethod

from apps.automode.app.dtos.juso_dto import (
    JusoContactCommand,
    JusoContactItem,
    JusoIntroduceQuery,
    JusoIntroduceResult,
)


class JusoPort(ABC):
    @abstractmethod
    async def introduce_myself(self, query: JusoIntroduceQuery) -> JusoIntroduceResult:
        """주소 검색 서비스 자기소개 레포지토리 추상 메소드"""
        pass

    @abstractmethod
    async def save_contacts(self, contacts: list[JusoContactCommand]) -> int:
        """연락처 일괄 저장"""
        pass

    @abstractmethod
    async def list_contacts(self) -> list[JusoContactItem]:
        """저장된 연락처 목록 조회"""
        pass
