from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..models.feedback_model import Feedback


class FeedbackRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create(self, row: Feedback) -> Feedback:
        self.session.add(row)
        await self.session.commit()
        await self.session.refresh(row)
        return row

    async def list_all(self) -> list[Feedback]:
        r = await self.session.execute(select(Feedback).order_by(Feedback.id.desc()))
        return list(r.scalars().all())
