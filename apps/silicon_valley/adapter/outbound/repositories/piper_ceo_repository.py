from __future__ import annotations

from sqlalchemy.ext.asyncio import AsyncSession

from apps.silicon_valley.app.dtos.piper_ceo_dto import PiperCeoQuery, PiperCeoResponse
from apps.silicon_valley.app.ports.output.piper_ceo_port import PiperCeoPort


class PiperCeoRepository(PiperCeoPort):

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def introduce_myself(self, query: PiperCeoQuery) -> PiperCeoResponse:
        return PiperCeoResponse(id=query.id, name=query.name)
