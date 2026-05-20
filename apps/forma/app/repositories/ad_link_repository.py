from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..models.ad_link_model import AdLink


class AdLinkRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create(self, row: AdLink) -> AdLink:
        self.session.add(row)
        await self.session.commit()
        await self.session.refresh(row)
        return row

    async def list_all(self) -> list[AdLink]:
        r = await self.session.execute(select(AdLink).order_by(AdLink.id.desc()))
        return list(r.scalars().all())
