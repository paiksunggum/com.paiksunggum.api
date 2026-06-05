from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..models.payment_logs_model import PaymentLog


class PaymentLogRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create(self, row: PaymentLog) -> PaymentLog:
        self.session.add(row)
        await self.session.commit()
        await self.session.refresh(row)
        return row

    async def list_all(self) -> list[PaymentLog]:
        result = await self.session.execute(select(PaymentLog).order_by(PaymentLog.id.desc()))
        return list(result.scalars().all())
