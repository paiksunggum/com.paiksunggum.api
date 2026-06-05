from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..models.users_ad_model import UsersAd


class UsersAdRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create(self, row: UsersAd) -> UsersAd:
        self.session.add(row)
        await self.session.commit()
        await self.session.refresh(row)
        return row

    async def list_all(self) -> list[UsersAd]:
        result = await self.session.execute(select(UsersAd).order_by(UsersAd.id.desc()))
        return list(result.scalars().all())
