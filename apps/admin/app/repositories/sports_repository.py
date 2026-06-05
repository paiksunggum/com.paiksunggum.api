from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..models.sports_model import Sport


class SportsRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create(self, row: Sport) -> Sport:
        self.session.add(row)
        await self.session.commit()
        await self.session.refresh(row)
        return row

    async def list_all(self) -> list[Sport]:
        result = await self.session.execute(select(Sport).order_by(Sport.id.desc()))
        return list(result.scalars().all())
