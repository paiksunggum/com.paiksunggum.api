from sqlalchemy.ext.asyncio import AsyncSession

from ..models.users_model import User
from ..repositories.users_repository import UsersRepository
from ..schemas.users_schema import FormaUserCreateRequest


class UsersService:
    def __init__(self, session: AsyncSession) -> None:
        self.users_repository = UsersRepository(session)

    async def create_user(self, req: FormaUserCreateRequest) -> User:
        existing = await self.users_repository.get_by_user_id(req.user_id)
        if existing is not None:
            raise ValueError("이미 사용 중인 user_id 입니다.")

        user = User(
            user_id=req.user_id,
            email=req.email,
            name=req.name,
            role=req.role,
        )
        return await self.users_repository.create(user)

    async def list_users(self) -> list[User]:
        return await self.users_repository.list_all()
