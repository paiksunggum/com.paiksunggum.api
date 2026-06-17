from __future__ import annotations

from sqlalchemy.ext.asyncio import AsyncSession

from apps.titanic.app.dtos.crew_hartley_violin_dto import HartleyViolinQuery, HartleyViolinResponse
from apps.titanic.app.ports.output.crew_hartley_violin_port import HartleyViolinPort


class HartleyViolinRepository(HartleyViolinPort):
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def introduce_myself(self, query: HartleyViolinQuery) -> HartleyViolinResponse:
        return HartleyViolinResponse(id=query.id * 10000, name=query.name)
