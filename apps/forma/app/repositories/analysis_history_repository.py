from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..models.analysis_history_model import AnalysisHistory


class AnalysisHistoryRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create(self, row: AnalysisHistory) -> AnalysisHistory:
        self.session.add(row)
        await self.session.commit()
        await self.session.refresh(row)
        return row

    async def get_by_id(self, history_id: int) -> AnalysisHistory | None:
        result = await self.session.execute(
            select(AnalysisHistory).where(AnalysisHistory.id == history_id)
        )
        return result.scalar_one_or_none()

    async def list_by_video_id(self, video_id: int) -> list[AnalysisHistory]:
        result = await self.session.execute(
            select(AnalysisHistory)
            .where(AnalysisHistory.video_id == video_id)
            .order_by(AnalysisHistory.id.desc())
        )
        return list(result.scalars().all())

    async def update(self, row: AnalysisHistory) -> AnalysisHistory:
        self.session.add(row)
        await self.session.commit()
        await self.session.refresh(row)
        return row
