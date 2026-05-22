from sqlalchemy.ext.asyncio import AsyncSession

from ..models.model_utils import now_utc
from ..models.user_skills_model import UserSkill
from ..repositories.user_skills_repository import UserSkillRepository
from ..schemas.user_skills_schema import UserSkillNestedCreateRequest


class UserSkillService:
    def __init__(self, session: AsyncSession) -> None:
        self.repository = UserSkillRepository(session)

    async def create_for_user(
        self, user_id: int, req: UserSkillNestedCreateRequest
    ) -> UserSkill:
        row = UserSkill(
            user_id=user_id,
            practice_id=req.practice_id,
            ai_level=req.ai_level,
            coach_level=req.coach_level,
            assessed_at=req.assessed_at or now_utc(),
        )
        return await self.repository.create(row)

    async def list_by_user(self, user_id: int) -> list[UserSkill]:
        return await self.repository.list_by_user_id(user_id)
