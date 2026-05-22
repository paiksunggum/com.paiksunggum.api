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

    async def list_by_video_id(self, video_id: int) -> list[Feedback]:
        result = await self.session.execute(
            select(Feedback)
            .where(Feedback.video_id == video_id)
            .order_by(Feedback.id.desc())
        )
        return list(result.scalars().all())

    async def get_by_id(self, feedback_id: int) -> Feedback | None:
        result = await self.session.execute(
            select(Feedback).where(Feedback.id == feedback_id)
        )
        return result.scalar_one_or_none()
