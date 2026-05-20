from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..models.video_model import Video


class VideoRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create(self, row: Video) -> Video:
        self.session.add(row)
        await self.session.commit()
        await self.session.refresh(row)
        return row

    async def list_all(self) -> list[Video]:
        result = await self.session.execute(select(Video).order_by(Video.id.desc()))
        return list(result.scalars().all())
