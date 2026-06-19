from __future__ import annotations

from sqlalchemy.ext.asyncio import AsyncSession

from apps.silicon_valley.app.dtos.piper_dash_dto import PiperDashQuery, PiperDashResponse
from apps.silicon_valley.app.ports.output.piper_dash_port import PiperDashPort


class PiperDashRepository(PiperDashPort):

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def introduce_myself(self, query: PiperDashQuery) -> PiperDashResponse:
        return PiperDashResponse(id=query.id, name=query.name)
