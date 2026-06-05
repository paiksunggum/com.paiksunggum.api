from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..models.subscription_plans_model import SubscriptionPlan


class SubscriptionPlansRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create(self, row: SubscriptionPlan) -> SubscriptionPlan:
        self.session.add(row)
        await self.session.commit()
        await self.session.refresh(row)
        return row

    async def list_all(self) -> list[SubscriptionPlan]:
        result = await self.session.execute(
            select(SubscriptionPlan).order_by(SubscriptionPlan.id.desc())
        )
        return list(result.scalars().all())

    async def get_by_plan_code(self, plan_code: str) -> SubscriptionPlan | None:
        result = await self.session.execute(
            select(SubscriptionPlan).where(SubscriptionPlan.plan_code == plan_code)
        )
        return result.scalar_one_or_none()
