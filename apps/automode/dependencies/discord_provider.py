from __future__ import annotations

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from apps.automode.adapter.outbound.repositories.discord_repository import (
    DiscordRepository,
)
from apps.automode.app.ports.input.discord_use_case import DiscordUseCase
from apps.automode.app.ports.output.discord_port import DiscordPort
from apps.automode.app.use_cases.discord_interactor import DiscordInteractor
from core.matrix.oracle_database import get_db


def get_discord_repository(
    db: AsyncSession = Depends(get_db),
) -> DiscordPort:
    return DiscordRepository(session=db)


def get_discord_use_case(
    repository: DiscordPort = Depends(get_discord_repository),
) -> DiscordUseCase:
    return DiscordInteractor(repository=repository)
