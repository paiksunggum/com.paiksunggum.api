from sqlalchemy.ext.asyncio import AsyncSession

from ..schemas.frame_schema import FrameCreateRequest
from ..services.frame_service import FrameService


class FrameController:
    def __init__(self, session: AsyncSession) -> None:
        self.service = FrameService(session)

    async def create_frame(self, req: FrameCreateRequest):
        return await self.service.create_frame(req)

    async def list_frames(self):
        return await self.service.list_frames()
