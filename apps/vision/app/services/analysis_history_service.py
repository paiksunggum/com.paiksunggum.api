from sqlalchemy.ext.asyncio import AsyncSession

from ..models.analysis_history_model import AnalysisHistory
from ..repositories.analysis_history_repository import AnalysisHistoryRepository
from ..schemas.analysis_history_schema import (
    AnalysisHistoryStartRequest,
    AnalysisHistoryUpdateRequest,
)


class AnalysisHistoryService:
    def __init__(self, session: AsyncSession) -> None:
        self.repository = AnalysisHistoryRepository(session)

    async def start_for_video(
        self, video_id: int, req: AnalysisHistoryStartRequest
    ) -> AnalysisHistory:
        row = AnalysisHistory(
            video_id=video_id,
            status=req.status,
            round_number=req.round_number,
            started_at=req.started_at,
            completed_at=req.completed_at,
        )
        return await self.repository.create(row)

    async def list_by_video(self, video_id: int) -> list[AnalysisHistory]:
        return await self.repository.list_by_video_id(video_id)

    async def update_history(
        self, history_id: int, req: AnalysisHistoryUpdateRequest
    ) -> AnalysisHistory:
        row = await self.repository.get_by_id(history_id)
        if row is None:
            raise ValueError("analysis_history 를 찾을 수 없습니다.")
        if req.status is not None:
            row.status = req.status
        if req.started_at is not None:
            row.started_at = req.started_at
        if req.completed_at is not None:
            row.completed_at = req.completed_at
        return await self.repository.update(row)
