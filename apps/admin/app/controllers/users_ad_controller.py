from sqlalchemy.ext.asyncio import AsyncSession

from ..schemas.users_ad_schema import UsersAdNestedCreateRequest
from ..services.users_ad_service import UsersAdService


class UsersAdController:
    def __init__(self, session: AsyncSession) -> None:
        self.service = UsersAdService(session)

    async def create_contract(self, user_id: int, req: UsersAdNestedCreateRequest):
        return await self.service.create_contract(user_id, req)
