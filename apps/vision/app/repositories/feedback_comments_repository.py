from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..models.feedback_comments_model import FeedbackComment


class FeedbackCommentRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create(self, row: FeedbackComment) -> FeedbackComment:
        self.session.add(row)
        await self.session.commit()
        await self.session.refresh(row)
        return row

    async def list_by_feedback_id(self, feedback_id: int) -> list[FeedbackComment]:
        result = await self.session.execute(
            select(FeedbackComment)
            .where(FeedbackComment.feedback_id == feedback_id)
            .order_by(FeedbackComment.id.asc())
        )
        return list(result.scalars().all())
