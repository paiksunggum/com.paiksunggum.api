from sqlalchemy.ext.asyncio import AsyncSession

from apps.silicon_valley.app.dtos.piper_hr_dto import PiperHrQuery, PiperHrResponse
from apps.silicon_valley.app.ports.output.piper_hr_port import PiperHrPort


class PiperHrRepository(PiperHrPort):

    def __init__(self, session: AsyncSession):
        self.session = session

    async def introduce_myself(self, query: PiperHrQuery) -> PiperHrResponse:
        return PiperHrResponse(id=query.id, name=query.name)
