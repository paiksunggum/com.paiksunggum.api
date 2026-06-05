from sqlalchemy.ext.asyncio import AsyncSession

from ..schemas.video_practice_match_schema import VideoPracticeMatchNestedCreateRequest
from ..services.video_practice_match_service import VideoPracticeMatchService


class VideoPracticeMatchController:
    def __init__(self, session: AsyncSession) -> None:
        self.service = VideoPracticeMatchService(session)

    async def create_for_video(
        self, video_id: int, req: VideoPracticeMatchNestedCreateRequest
    ):
        return await self.service.create_for_video(video_id, req)
