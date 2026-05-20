from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..models.ads_model import Ad


class AdsRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create(self, row: Ad) -> Ad:
        self.session.add(row)
        await self.session.commit()
        await self.session.refresh(row)
        return row

    async def list_all(self) -> list[Ad]:
        r = await self.session.execute(select(Ad).order_by(Ad.id.desc()))
        return list(r.scalars().all())
