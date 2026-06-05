from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..models.practice_model import Practice


class PracticeRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create(self, row: Practice) -> Practice:
        self.session.add(row)
        await self.session.commit()
        await self.session.refresh(row)
        return row

    async def list_by_sport_id(self, sport_id: int) -> list[Practice]:
        result = await self.session.execute(
            select(Practice)
            .where(Practice.sports_id == sport_id)
            .order_by(Practice.id.desc())
        )
        return list(result.scalars().all())

    async def list_active(self) -> list[Practice]:
        result = await self.session.execute(
            select(Practice)
            .where(Practice.is_active.is_(True))
            .order_by(Practice.id.desc())
        )
        return list(result.scalars().all())
