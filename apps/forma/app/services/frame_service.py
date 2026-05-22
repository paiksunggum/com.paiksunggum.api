from sqlalchemy.ext.asyncio import AsyncSession

from ..models.frame_model import Frame
from ..repositories.analysis_history_repository import AnalysisHistoryRepository
from ..repositories.frame_repository import FrameRepository
from ..schemas.frame_schema import FrameNestedCreateRequest


class FrameService:
    def __init__(self, session: AsyncSession) -> None:
        self.frame_repository = FrameRepository(session)
        self.history_repository = AnalysisHistoryRepository(session)

    async def create_for_history(
        self, history_id: int, req: FrameNestedCreateRequest
    ) -> Frame:
        history = await self.history_repository.get_by_id(history_id)
        if history is None:
            raise ValueError("analysis_history 를 찾을 수 없습니다.")
        row = Frame(
            analysis_history_id=history_id,
            video_id=history.video_id,
            frame_index=req.frame_index,
            timestamp_sec=req.timestamp_sec,
            keypoints=req.keypoints,
        )
        return await self.frame_repository.create(row)

    async def list_by_history(self, history_id: int) -> list[Frame]:
        return await self.frame_repository.list_by_analysis_history_id(history_id)
