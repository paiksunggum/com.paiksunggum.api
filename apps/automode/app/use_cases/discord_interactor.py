from __future__ import annotations

from apps.automode.app.dtos.discord_dto import (
    DiscordIntroduceQuery,
    DiscordIntroduceResult,
)
from apps.automode.app.ports.input.i_discord_use_case import IDiscordUseCase
from apps.automode.app.ports.output.i_discord_port import IDiscordPort


class DiscordInteractor(IDiscordUseCase):
    def __init__(self, repository: IDiscordPort) -> None:
        self._repository = repository

    async def introduce_myself(
        self, query: DiscordIntroduceQuery
    ) -> DiscordIntroduceResult:
        return await self._repository.introduce_myself(query)
