from sqlalchemy.ext.asyncio import AsyncSession

from ..models.video_practice_match_model import VideoPracticeMatch
from ..repositories.video_practice_match_repository import VideoPracticeMatchRepository
from ..schemas.video_practice_match_schema import VideoPracticeMatchNestedCreateRequest


class VideoPracticeMatchService:
    def __init__(self, session: AsyncSession) -> None:
        self.repository = VideoPracticeMatchRepository(session)

    async def create_for_video(
        self, video_id: int, req: VideoPracticeMatchNestedCreateRequest
    ) -> VideoPracticeMatch:
        row = VideoPracticeMatch(
            video_id=video_id,
            practice_id=req.practice_id,
            match_score=req.match_score,
        )
        return await self.repository.create(row)
