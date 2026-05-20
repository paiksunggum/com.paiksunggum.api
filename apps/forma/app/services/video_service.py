from sqlalchemy.ext.asyncio import AsyncSession

from ..models.video_model import Video
from ..repositories.video_repository import VideoRepository
from ..schemas.video_schema import VideoCreateRequest


class VideoService:
    def __init__(self, session: AsyncSession) -> None:
        self.video_repository = VideoRepository(session)

    async def create_video(self, req: VideoCreateRequest) -> Video:
        row = Video(
            user_id=req.user_id,
            sport_id=req.sport_id,
            title=req.title,
            video_url=req.video_url,
            duration_sec=req.duration_sec,
            visibility=req.visibility,
        )
        return await self.video_repository.create(row)

    async def list_videos(self) -> list[Video]:
        return await self.video_repository.list_all()
