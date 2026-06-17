from __future__ import annotations

from typing import Any

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from apps.titanic.adapter.outbound.orm.passenger_rose_model_orm import RoseModelORM
from apps.titanic.adapter.outbound.orm.passenger_jack_trainer_orm import JackTrainerORM
from apps.titanic.app.dtos.passenger_rose_model_dto import RoseModelQuery, RoseModelResponse
from apps.titanic.app.ports.output.passenger_rose_model_port import RoseModelPort

class RoseModelRepository(RoseModelPort):
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def introduce_myself(self, query: RoseModelQuery) -> RoseModelResponse:
        return RoseModelResponse(id=query.id * 10000, name=query.name + "가 레포지토리에 다녀옴")