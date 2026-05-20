from sqlalchemy.ext.asyncio import AsyncSession

from ..schemas.feedback_schema import FeedbackCreateRequest
from ..services.feedback_service import FeedbackService


class FeedbackController:
    def __init__(self, session: AsyncSession) -> None:
        self.service = FeedbackService(session)

    async def create_feedback(self, req: FeedbackCreateRequest):
        return await self.service.create_feedback(req)

    async def list_feedbacks(self):
        return await self.service.list_feedbacks()
