from sqlalchemy.ext.asyncio import AsyncSession

from ..schemas.subscription_plans_schema import SubscriptionPlanCreateRequest
from ..services.subscription_plans_service import SubscriptionPlansService


class SubscriptionPlansController:
    def __init__(self, session: AsyncSession) -> None:
        self.service = SubscriptionPlansService(session)

    async def create_plan(self, req: SubscriptionPlanCreateRequest):
        return await self.service.create_plan(req)

    async def list_plans(self):
        return await self.service.list_plans()
