from sqlalchemy.ext.asyncio import AsyncSession

from ..models.payment_logs_model import PaymentLog
from ..repositories.payment_logs_repository import PaymentLogRepository
from ..schemas.payment_logs_schema import PaymentLogNestedCreateRequest


class PaymentLogService:
    def __init__(self, session: AsyncSession) -> None:
        self.repository = PaymentLogRepository(session)

    async def create_for_subscription(
        self, subscription_id: int, req: PaymentLogNestedCreateRequest
    ) -> PaymentLog:
        row = PaymentLog(
            subscription_id=subscription_id,
            user_id=req.user_id,
            amount_cents=req.amount_cents,
            currency=req.currency,
            pg_transaction_id=req.pg_transaction_id,
            status=req.status,
            paid_at=req.paid_at,
        )
        return await self.repository.create(row)
