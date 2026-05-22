from sqlalchemy.ext.asyncio import AsyncSession

from ..schemas.user_skills_schema import UserSkillNestedCreateRequest
from ..services.user_skills_service import UserSkillService


class UserSkillController:
    def __init__(self, session: AsyncSession) -> None:
        self.service = UserSkillService(session)

    async def create_for_user(self, user_id: int, req: UserSkillNestedCreateRequest):
        return await self.service.create_for_user(user_id, req)

    async def list_by_user(self, user_id: int):
        return await self.service.list_by_user(user_id)
