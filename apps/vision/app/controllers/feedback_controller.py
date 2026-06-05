from sqlalchemy.ext.asyncio import AsyncSession

from ..schemas.feedback_schema import FeedbackNestedCreateRequest
from ..services.feedback_service import FeedbackService


class FeedbackController:
    def __init__(self, session: AsyncSession) -> None:
        self.service = FeedbackService(session)

    async def create_for_video(self, video_id: int, req: FeedbackNestedCreateRequest):
        return await self.service.create_for_video(video_id, req)

    async def list_by_video(self, video_id: int):
        return await self.service.list_by_video(video_id)
