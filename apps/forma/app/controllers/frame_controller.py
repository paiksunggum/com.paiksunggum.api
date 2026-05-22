from sqlalchemy.ext.asyncio import AsyncSession

from ..schemas.frame_schema import FrameNestedCreateRequest
from ..services.frame_service import FrameService


class FrameController:
    def __init__(self, session: AsyncSession) -> None:
        self.service = FrameService(session)

    async def create_for_history(self, history_id: int, req: FrameNestedCreateRequest):
        return await self.service.create_for_history(history_id, req)

    async def list_by_history(self, history_id: int):
        return await self.service.list_by_history(history_id)
