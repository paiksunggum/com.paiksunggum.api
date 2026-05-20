from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..models.subscriptions_model import Subscription


class SubscriptionsRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create(self, row: Subscription) -> Subscription:
        self.session.add(row)
        await self.session.commit()
        await self.session.refresh(row)
        return row

    async def list_all(self) -> list[Subscription]:
        r = await self.session.execute(
            select(Subscription).order_by(Subscription.id.desc())
        )
        return list(r.scalars().all())
