from sqlalchemy.ext.asyncio import AsyncSession

from ..schemas.subscriptions_schema import SubscriptionNestedCreateRequest
from ..services.subscriptions_service import SubscriptionsService


class SubscriptionsController:
    def __init__(self, session: AsyncSession) -> None:
        self.service = SubscriptionsService(session)

    async def create_for_user(self, user_id: int, req: SubscriptionNestedCreateRequest):
        return await self.service.create_for_user(user_id, req)

    async def get_active_for_user(self, user_id: int):
        return await self.service.get_active_for_user(user_id)
