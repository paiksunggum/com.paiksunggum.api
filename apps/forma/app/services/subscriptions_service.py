from sqlalchemy.ext.asyncio import AsyncSession

from ..models.subscriptions_model import Subscription
from ..repositories.subscriptions_repository import SubscriptionsRepository
from ..schemas.subscriptions_schema import SubscriptionCreateRequest


class SubscriptionsService:
    def __init__(self, session: AsyncSession) -> None:
        self.subscriptions_repository = SubscriptionsRepository(session)

    async def create_subscription(self, req: SubscriptionCreateRequest) -> Subscription:
        row = Subscription(
            subscriber_user_id=req.subscriber_user_id,
            creator_user_id=req.creator_user_id,
            status=req.status,
            ended_at=req.ended_at,
        )
        return await self.subscriptions_repository.create(row)

    async def list_subscriptions(self) -> list[Subscription]:
        return await self.subscriptions_repository.list_all()
