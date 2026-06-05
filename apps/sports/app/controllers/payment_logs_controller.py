from sqlalchemy.ext.asyncio import AsyncSession

from ..schemas.payment_logs_schema import PaymentLogNestedCreateRequest
from ..services.payment_logs_service import PaymentLogService


class PaymentLogController:
    def __init__(self, session: AsyncSession) -> None:
        self.service = PaymentLogService(session)

    async def create_for_subscription(
        self, subscription_id: int, req: PaymentLogNestedCreateRequest
    ):
        return await self.service.create_for_subscription(subscription_id, req)
