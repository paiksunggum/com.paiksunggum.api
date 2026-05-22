from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..models.user_skills_model import UserSkill


class UserSkillRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create(self, row: UserSkill) -> UserSkill:
        self.session.add(row)
        await self.session.commit()
        await self.session.refresh(row)
        return row

    async def list_by_user_id(self, user_id: int) -> list[UserSkill]:
        result = await self.session.execute(
            select(UserSkill)
            .where(UserSkill.user_id == user_id)
            .order_by(UserSkill.id.desc())
        )
        return list(result.scalars().all())
