from __future__ import annotations

from abc import ABC, abstractmethod

from apps.automode.app.dtos.juso_dto import (
    JusoContactCommand,
    JusoContactItem,
    JusoContactUploadResult,
    JusoIntroduceQuery,
    JusoIntroduceResult,
)


class IJusoUseCase(ABC):
    @abstractmethod
    async def introduce_myself(self, query: JusoIntroduceQuery) -> JusoIntroduceResult:
        """주소 검색 서비스 자기소개"""
        pass

    @abstractmethod
    async def upload_contacts(
        self, contacts: list[JusoContactCommand]
    ) -> JusoContactUploadResult:
        """Google 주소록 CSV 업로드"""
        pass

    @abstractmethod
    async def list_contacts(self) -> list[JusoContactItem]:
        """저장된 연락처 목록 조회"""
        pass
