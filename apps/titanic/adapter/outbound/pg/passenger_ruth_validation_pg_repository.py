from __future__ import annotations

from typing import Any

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from apps.titanic.adapter.outbound.orm.booking_orm import BookingORM
from apps.titanic.adapter.outbound.orm.person_orm import PersonORM
from apps.titanic.app.dtos.passenger_ruth_validation_dto import RuthValidationQuery, RuthValidationResponse
from apps.titanic.app.ports.output.passenger_ruth_validation_repository import RuthValidationRepository



class RuthValidationPgRepository(RuthValidationRepository):
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def introduce_myself(self, query: RuthValidationQuery) -> RuthValidationResponse:
        return RuthValidationResponse(id=query.id * 10000, name=query.name)
