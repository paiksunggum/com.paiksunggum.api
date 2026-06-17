from __future__ import annotations

from sqlalchemy.ext.asyncio import AsyncSession

from apps.titanic.app.dtos.passenger_cal_tester_dto import CalTestQuery, CalTestResponse
from apps.titanic.app.ports.output.passenger_cal_tester_port import CalTestPort


class CalTesterRepository(CalTestPort):
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def introduce_myself(self, query: CalTestQuery) -> CalTestResponse:
        return CalTestResponse(id=query.id * 10000, name=query.name)
