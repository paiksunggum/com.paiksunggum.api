from __future__ import annotations

from sqlalchemy.ext.asyncio import AsyncSession

from apps.titanic.app.dtos.crew_lowe_boat_dto import LoweBoatQuery, LoweBoatResponse
from apps.titanic.app.ports.output.crew_lowe_boat_repository import LoweBoatRepository


class LoweBoatPgRepository(LoweBoatRepository):
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def introduce_myself(self, query: LoweBoatQuery) -> LoweBoatResponse:
        return LoweBoatResponse(id=query.id * 10000, name=query.name)
