from sqlalchemy.ext.asyncio import AsyncSession

from ..schemas.analysis_history_schema import (
    AnalysisHistoryStartRequest,
    AnalysisHistoryUpdateRequest,
)
from ..services.analysis_history_service import AnalysisHistoryService


class AnalysisHistoryController:
    def __init__(self, session: AsyncSession) -> None:
        self.service = AnalysisHistoryService(session)

    async def start_for_video(self, video_id: int, req: AnalysisHistoryStartRequest):
        return await self.service.start_for_video(video_id, req)

    async def list_by_video(self, video_id: int):
        return await self.service.list_by_video(video_id)

    async def update_history(self, history_id: int, req: AnalysisHistoryUpdateRequest):
        return await self.service.update_history(history_id, req)
