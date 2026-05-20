from sqlalchemy.ext.asyncio import AsyncSession

from ..schemas.users_schema import FormaUserCreateRequest
from ..services.users_service import UsersService


class UsersController:
    def __init__(self, session: AsyncSession) -> None:
        self.service = UsersService(session)

    async def create_user(self, req: FormaUserCreateRequest):
        return await self.service.create_user(req)

    async def list_users(self):
        return await self.service.list_users()
