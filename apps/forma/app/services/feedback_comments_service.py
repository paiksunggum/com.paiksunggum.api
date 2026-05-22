from sqlalchemy.ext.asyncio import AsyncSession

from ..models.feedback_comments_model import FeedbackComment
from ..repositories.feedback_comments_repository import FeedbackCommentRepository
from ..repositories.feedback_repository import FeedbackRepository
from ..schemas.feedback_comments_schema import FeedbackCommentNestedCreateRequest


class FeedbackCommentService:
    def __init__(self, session: AsyncSession) -> None:
        self.repository = FeedbackCommentRepository(session)
        self.feedback_repository = FeedbackRepository(session)

    async def create_for_feedback(
        self, feedback_id: int, req: FeedbackCommentNestedCreateRequest
    ) -> FeedbackComment:
        feedback = await self.feedback_repository.get_by_id(feedback_id)
        if feedback is None:
            raise ValueError("feedback 를 찾을 수 없습니다.")
        row = FeedbackComment(
            feedback_id=feedback_id,
            user_id=req.user_id,
            parent_comment_id=req.parent_comment_id,
            body=req.body,
        )
        return await self.repository.create(row)

    async def list_by_feedback(self, feedback_id: int) -> list[FeedbackComment]:
        return await self.repository.list_by_feedback_id(feedback_id)
