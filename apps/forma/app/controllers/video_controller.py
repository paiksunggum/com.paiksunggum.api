from sqlalchemy.ext.asyncio import AsyncSession

from ..schemas.video_schema import VideoCreateRequest
from ..services.video_service import VideoService


class VideoController:
    def __init__(self, session: AsyncSession) -> None:
        self.service = VideoService(session)

    async def create_video(self, req: VideoCreateRequest):
        return await self.service.create_video(req)

    async def list_videos(self):
        return await self.service.list_videos()
