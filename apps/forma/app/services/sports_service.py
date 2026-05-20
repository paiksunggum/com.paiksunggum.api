from sqlalchemy.ext.asyncio import AsyncSession

from ..models.sports_model import Sport
from ..repositories.sports_repository import SportsRepository
from ..schemas.sports_schema import SportCreateRequest


class SportsService:
    def __init__(self, session: AsyncSession) -> None:
        self.sports_repository = SportsRepository(session)

    async def create_sport(self, req: SportCreateRequest) -> Sport:
        row = Sport(
            name=req.name,
            description=req.description,
            is_active=req.is_active,
        )
        return await self.sports_repository.create(row)

    async def list_sports(self) -> list[Sport]:
        return await self.sports_repository.list_all()
