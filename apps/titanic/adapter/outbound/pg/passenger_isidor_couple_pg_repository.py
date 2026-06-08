from __future__ import annotations

from sqlalchemy.ext.asyncio import AsyncSession

from apps.titanic.app.dtos.passenger_isidor_couple_dto import IsidorCoupleQuery, IsidorCoupleResponse
from apps.titanic.app.ports.output.passenger_isidor_couple_repository import IsidorCoupleRepository


class IsidorCouplePgRepository(IsidorCoupleRepository):
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def introduce_myself(self, query: IsidorCoupleQuery) -> IsidorCoupleResponse:
        return IsidorCoupleResponse(id=query.id * 10000, name=query.name)
