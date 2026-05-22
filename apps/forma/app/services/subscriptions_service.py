from sqlalchemy.ext.asyncio import AsyncSession

from ..models.subscriptions_model import Subscription
from ..repositories.subscriptions_repository import SubscriptionsRepository
from ..schemas.subscriptions_schema import SubscriptionNestedCreateRequest


class SubscriptionsService:
    def __init__(self, session: AsyncSession) -> None:
        self.subscriptions_repository = SubscriptionsRepository(session)

    async def create_for_user(
        self, user_id: int, req: SubscriptionNestedCreateRequest
    ) -> Subscription:
        row = Subscription(
            user_id=user_id,
            plan_code=req.plan_code,
            status=req.status,
            ended_at=req.ended_at,
        )
        return await self.subscriptions_repository.create(row)

    async def get_active_for_user(self, user_id: int) -> Subscription | None:
        return await self.subscriptions_repository.get_active_by_user_id(user_id)
