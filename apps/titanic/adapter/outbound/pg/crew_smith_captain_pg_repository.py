from __future__ import annotations

from typing import Any

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from apps.titanic.adapter.outbound.orm.passenger_jack_trainer_orm import JackTrainerORM
from apps.titanic.app.dtos.crew_smith_captain_dto import SmithCaptainQuery, SmithCaptainResponse
from apps.titanic.app.ports.output.crew_smith_captain_repository import SmithCaptainRepository


class SmithCaptainPgRepository(SmithCaptainRepository):
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def introduce_myself(self, query: SmithCaptainQuery) -> SmithCaptainResponse:
        return SmithCaptainResponse(id=query.id * 10000, name=query.name)
