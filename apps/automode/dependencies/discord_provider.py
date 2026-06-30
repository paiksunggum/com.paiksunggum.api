from __future__ import annotations

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from apps.automode.adapter.outbound.repositories.discord_repository import (
    DiscordRepository,
)
from apps.automode.app.ports.input.i_discord_use_case import IDiscordUseCase
from apps.automode.app.ports.output.i_discord_port import IDiscordPort
from apps.automode.app.use_cases.discord_interactor import DiscordInteractor
from core.matrix.oracle_database import get_db


def get_discord_repository(
    db: AsyncSession = Depends(get_db),
) -> IDiscordPort:
    return DiscordRepository(session=db)


def get_discord_use_case(
    repository: IDiscordPort = Depends(get_discord_repository),
) -> IDiscordUseCase:
    return DiscordInteractor(repository=repository)
