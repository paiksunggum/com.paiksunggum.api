from __future__ import annotations

from abc import ABC, abstractmethod

from apps.automode.app.dtos.discord_dto import (
    DiscordIntroduceQuery,
    DiscordIntroduceResult,
)


class DiscordPort(ABC):
    @abstractmethod
    async def introduce_myself(
        self, query: DiscordIntroduceQuery
    ) -> DiscordIntroduceResult:
        """Discord 서비스 자기소개 레포지토리 추상 메소드"""
        pass
