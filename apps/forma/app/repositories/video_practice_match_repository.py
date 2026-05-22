from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..models.video_practice_match_model import VideoPracticeMatch


class VideoPracticeMatchRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create(self, row: VideoPracticeMatch) -> VideoPracticeMatch:
        self.session.add(row)
        await self.session.commit()
        await self.session.refresh(row)
        return row

    async def list_all(self) -> list[VideoPracticeMatch]:
        result = await self.session.execute(select(VideoPracticeMatch).order_by(VideoPracticeMatch.id.desc()))
        return list(result.scalars().all())
