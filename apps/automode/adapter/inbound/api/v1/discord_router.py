from __future__ import annotations

import logging

from fastapi import APIRouter, Depends

from apps.automode.adapter.inbound.api.schemas.discord_schema import (
    DiscordIntroduceResponseSchema,
)
from apps.automode.app.dtos.discord_dto import DiscordIntroduceQuery
from apps.automode.app.ports.input.discord_use_case import DiscordUseCase
from apps.automode.dependencies.discord_provider import get_discord_use_case

logger = logging.getLogger("apps")
discord_router = APIRouter(prefix="/discord", tags=["automode"])


@discord_router.get("/myself", response_model=DiscordIntroduceResponseSchema)
async def introduce_myself(
    use_case: DiscordUseCase = Depends(get_discord_use_case),
) -> DiscordIntroduceResponseSchema:
    logger.info("[automode] Discord 서비스 자기소개 요청")
    result = await use_case.introduce_myself(
        DiscordIntroduceQuery(id=2, name="Discord")
    )
    return DiscordIntroduceResponseSchema(id=result.id, name=result.name)
