from sqlalchemy.ext.asyncio import AsyncSession

from ..models.feedback_model import Feedback
from ..repositories.feedback_repository import FeedbackRepository
from ..schemas.feedback_schema import FeedbackCreateRequest


class FeedbackService:
    def __init__(self, session: AsyncSession) -> None:
        self.feedback_repository = FeedbackRepository(session)

    async def create_feedback(self, req: FeedbackCreateRequest) -> Feedback:
        row = Feedback(
            video_id=req.video_id,
            frame_id=req.frame_id,
            source_type=req.source_type,
            comment=req.comment,
            score=req.score,
        )
        return await self.feedback_repository.create(row)

    async def list_feedbacks(self) -> list[Feedback]:
        return await self.feedback_repository.list_all()
