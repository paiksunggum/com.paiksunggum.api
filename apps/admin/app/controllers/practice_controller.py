from sqlalchemy.ext.asyncio import AsyncSession

from ..schemas.practice_schema import PracticeCreateRequest
from ..services.practice_service import PracticeService


class PracticeController:
    def __init__(self, session: AsyncSession) -> None:
        self.service = PracticeService(session)

    async def create_practice(self, req: PracticeCreateRequest):
        return await self.service.create_practice(req)

    async def list_practices(self, sport_id: int | None = None):
        return await self.service.list_practices(sport_id)
