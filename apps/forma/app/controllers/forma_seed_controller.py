from sqlalchemy.ext.asyncio import AsyncSession

from ..services.forma_seed_service import FormaSeedService


class FormaSeedController:
    def __init__(self, session: AsyncSession) -> None:
        self.service = FormaSeedService(session)

    async def seed_demo_from_country_csv(self, limit: int = 15):
        return await self.service.seed_demo_from_country_csv(limit=limit)
