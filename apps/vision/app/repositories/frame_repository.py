from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..models.frame_model import Frame


class FrameRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create(self, row: Frame) -> Frame:
        self.session.add(row)
        await self.session.commit()
        await self.session.refresh(row)
        return row

    async def list_by_analysis_history_id(
        self, analysis_history_id: int
    ) -> list[Frame]:
        result = await self.session.execute(
            select(Frame)
            .where(Frame.analysis_history_id == analysis_history_id)
            .order_by(Frame.frame_index.asc())
        )
        return list(result.scalars().all())
