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

    async def get_active_by_user_id(self, user_id: int) -> Subscription | None:
        result = await self.session.execute(
            select(Subscription)
            .where(
                Subscription.user_id == user_id,
                Subscription.status == "active",
            )
            .order_by(Subscription.id.desc())
            .limit(1)
        )
        return result.scalar_one_or_none()
