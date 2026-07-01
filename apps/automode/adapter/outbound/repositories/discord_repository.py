from __future__ import annotations

from sqlalchemy.ext.asyncio import AsyncSession

from apps.automode.app.dtos.discord_dto import (
    DiscordIntroduceQuery,
    DiscordIntroduceResult,
)
from apps.automode.app.ports.output.discord_port import DiscordPort


class DiscordRepository(DiscordPort):
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def introduce_myself(
        self, query: DiscordIntroduceQuery
    ) -> DiscordIntroduceResult:
        return DiscordIntroduceResult(id=query.id, name="Discord 봇 서비스")
