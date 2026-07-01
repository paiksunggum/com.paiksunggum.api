from __future__ import annotations

from apps.automode.app.dtos.discord_dto import (
    DiscordIntroduceQuery,
    DiscordIntroduceResult,
)
from apps.automode.app.ports.input.discord_use_case import DiscordUseCase
from apps.automode.app.ports.output.discord_port import DiscordPort


class DiscordInteractor(DiscordUseCase):
    def __init__(self, repository: DiscordPort) -> None:
        self._repository = repository

    async def introduce_myself(
        self, query: DiscordIntroduceQuery
    ) -> DiscordIntroduceResult:
        return await self._repository.introduce_myself(query)
