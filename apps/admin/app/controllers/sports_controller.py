from sqlalchemy.ext.asyncio import AsyncSession

from ..schemas.sports_schema import SportCreateRequest
from ..services.sports_service import SportsService


class SportsController:
    def __init__(self, session: AsyncSession) -> None:
        self.service = SportsService(session)

    async def create_sport(self, req: SportCreateRequest):
        return await self.service.create_sport(req)

    async def list_sports(self):
        return await self.service.list_sports()
