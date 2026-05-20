from sqlalchemy.ext.asyncio import AsyncSession

from ..models.frame_model import Frame
from ..repositories.frame_repository import FrameRepository
from ..schemas.frame_schema import FrameCreateRequest


class FrameService:
    def __init__(self, session: AsyncSession) -> None:
        self.frame_repository = FrameRepository(session)

    async def create_frame(self, req: FrameCreateRequest) -> Frame:
        row = Frame(
            video_id=req.video_id,
            frame_index=req.frame_index,
            timestamp_sec=req.timestamp_sec,
            pose_json=req.pose_json,
        )
        return await self.frame_repository.create(row)

    async def list_frames(self) -> list[Frame]:
        return await self.frame_repository.list_all()
