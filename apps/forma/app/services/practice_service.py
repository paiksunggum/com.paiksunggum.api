from sqlalchemy.ext.asyncio import AsyncSession

from ..models.practice_model import Practice
from ..repositories.practice_repository import PracticeRepository
from ..schemas.practice_schema import PracticeCreateRequest


class PracticeService:
    def __init__(self, session: AsyncSession) -> None:
        self.practice_repository = PracticeRepository(session)

    async def create_practice(self, req: PracticeCreateRequest) -> Practice:
        row = Practice(
            sports_id=req.sports_id,
            title=req.title,
            description=req.description,
            guide_json=req.guide_json,
            is_active=req.is_active,
        )
        return await self.practice_repository.create(row)

    async def list_practices(
        self, sport_id: int | None = None
    ) -> list[Practice]:
        if sport_id is not None:
            return await self.practice_repository.list_by_sport_id(sport_id)
        return await self.practice_repository.list_active()
