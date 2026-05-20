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

    async def list_all(self) -> list[Practice]:
        r = await self.session.execute(select(Practice).order_by(Practice.id.desc()))
        return list(r.scalars().all())
