from sqlalchemy.ext.asyncio import AsyncSession

from ..schemas.subscriptions_schema import SubscriptionCreateRequest
from ..services.subscriptions_service import SubscriptionsService


class SubscriptionsController:
    def __init__(self, session: AsyncSession) -> None:
        self.service = SubscriptionsService(session)

    async def create_subscription(self, req: SubscriptionCreateRequest):
        return await self.service.create_subscription(req)

    async def list_subscriptions(self):
        return await self.service.list_subscriptions()
