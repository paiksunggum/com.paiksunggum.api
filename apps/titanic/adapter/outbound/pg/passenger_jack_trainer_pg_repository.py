from __future__ import annotations

from typing import Any

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from apps.titanic.adapter.outbound.orm.passenger_rose_model_orm import RoseModelORM
from apps.titanic.adapter.outbound.orm.passenger_jack_trainer_orm import JackTrainerORM
from apps.titanic.app.dtos.passenger_jack_trainer_dto import JackTrainerQuery, JackTrainerResponse
from apps.titanic.app.ports.output.passenger_jack_trainer_repository import JackTrainerRepository


class JackTrainerPgRepository(JackTrainerRepository):
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def introduce_myself(self, query: JackTrainerQuery) -> JackTrainerResponse:
        return JackTrainerResponse(id=query.id * 10000, name=query.name)

