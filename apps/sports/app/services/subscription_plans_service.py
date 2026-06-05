from sqlalchemy.ext.asyncio import AsyncSession

from ..models.subscription_plans_model import SubscriptionPlan
from ..repositories.subscription_plans_repository import SubscriptionPlansRepository
from ..schemas.subscription_plans_schema import SubscriptionPlanCreateRequest


class SubscriptionPlansService:
    def __init__(self, session: AsyncSession) -> None:
        self.repository = SubscriptionPlansRepository(session)

    async def create_plan(self, req: SubscriptionPlanCreateRequest) -> SubscriptionPlan:
        row = SubscriptionPlan(
            plan_code=req.plan_code,
            name=req.name,
            description=req.description,
            price_cents=req.price_cents,
            currency=req.currency,
            billing_interval=req.billing_interval,
            is_active=req.is_active,
        )
        return await self.repository.create(row)

    async def list_plans(self) -> list[SubscriptionPlan]:
        return await self.repository.list_all()
