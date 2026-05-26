from sqlalchemy.ext.asyncio import AsyncSession

from ..models.feedback_model import Feedback
from ..repositories.feedback_repository import FeedbackRepository
from ..schemas.feedback_schema import FeedbackNestedCreateRequest


class FeedbackService:
    def __init__(self, session: AsyncSession) -> None:
        self.feedback_repository = FeedbackRepository(session)

    async def create_for_video(
        self, video_id: int, req: FeedbackNestedCreateRequest
    ) -> Feedback:
        if req.frame_id is not None:
            row = Feedback(
                video_id=None,
                frame_id=req.frame_id,
                source_type=req.source_type,
                comment=req.comment,
                score=req.score,
            )
        else:
            row = Feedback(
                video_id=video_id,
                frame_id=None,
                source_type=req.source_type,
                comment=req.comment,
                score=req.score,
            )
        return await self.feedback_repository.create(row)

    async def list_by_video(self, video_id: int) -> list[Feedback]:
        return await self.feedback_repository.list_by_video_id(video_id)
