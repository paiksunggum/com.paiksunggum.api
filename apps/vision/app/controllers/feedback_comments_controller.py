from sqlalchemy.ext.asyncio import AsyncSession

from ..schemas.feedback_comments_schema import FeedbackCommentNestedCreateRequest
from ..services.feedback_comments_service import FeedbackCommentService


class FeedbackCommentController:
    def __init__(self, session: AsyncSession) -> None:
        self.service = FeedbackCommentService(session)

    async def create_for_feedback(
        self, feedback_id: int, req: FeedbackCommentNestedCreateRequest
    ):
        return await self.service.create_for_feedback(feedback_id, req)

    async def list_by_feedback(self, feedback_id: int):
        return await self.service.list_by_feedback(feedback_id)
