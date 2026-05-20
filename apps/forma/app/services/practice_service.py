from sqlalchemy.ext.asyncio import AsyncSession

from ..models.practice_model import Practice
from ..repositories.practice_repository import PracticeRepository
from ..schemas.practice_schema import PracticeCreateRequest


class PracticeService:
    def __init__(self, session: AsyncSession) -> None:
        self.practice_repository = PracticeRepository(session)

    async def create_practice(self, req: PracticeCreateRequest) -> Practice:
        row = Practice(
            user_id=req.user_id,
            sport_id=req.sport_id,
            video_id=req.video_id,
            note=req.note,
        )
        return await self.practice_repository.create(row)

    async def list_practices(self) -> list[Practice]:
        return await self.practice_repository.list_all()
