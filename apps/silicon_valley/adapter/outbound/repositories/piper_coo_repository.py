from sqlalchemy.ext.asyncio import AsyncSession

from apps.silicon_valley.app.dtos.piper_coo_dto import PiperCooQuery, PiperCooResponse
from apps.silicon_valley.app.ports.output.piper_coo_port import PiperCooPort


class PiperCooRepository(PiperCooPort):

    def __init__(self, session: AsyncSession):
        self.session = session

    async def introduce_myself(self, query: PiperCooQuery) -> PiperCooResponse:
        return PiperCooResponse(id=query.id, name=query.name)
