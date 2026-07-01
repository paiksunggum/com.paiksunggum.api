from __future__ import annotations

from abc import ABC, abstractmethod

from apps.automode.app.dtos.email_request_dto import (
    EmailIntroduceQuery,
    EmailIntroduceResult,
)


class EmailIntroduceUseCase(ABC):
    @abstractmethod
    async def introduce_myself(
        self, query: EmailIntroduceQuery
    ) -> EmailIntroduceResult:
        """이메일 서비스 자기소개"""
        pass
