from sqlalchemy.ext.asyncio import AsyncSession

from apps.silicon_valley.app.dtos.piper_sys_dto import PiperSysQuery, PiperSysResponse
from apps.silicon_valley.app.ports.output.piper_sys_port import PiperSysPort


class PiperSysRepository(PiperSysPort):

    def __init__(self, session: AsyncSession):
        self.session = session

    async def introduce_myself(self, query: PiperSysQuery) -> PiperSysResponse:
        return PiperSysResponse(id=query.id, name=query.name)
