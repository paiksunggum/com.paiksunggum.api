import secrets

from sqlalchemy.ext.asyncio import AsyncSession

from apps.friday13th.app.security import hash_password

from ..models.users_model import User
from ..repositories.users_repository import UsersRepository
from ..schemas.users_schema import FormaUserCreateRequest


class UsersService:
    def __init__(self, session: AsyncSession) -> None:
        self.users_repository = UsersRepository(session)

    async def create_user(self, req: FormaUserCreateRequest) -> User:
        existing = await self.users_repository.get_by_login_id(req.login_id)
        if existing is not None:
            raise ValueError("이미 사용 중인 login_id 입니다.")

        user = User(
            login_id=req.login_id,
            password_hash=hash_password(secrets.token_urlsafe(32)),
            email=req.email,
            name=req.name,
            birthdate=req.birthdate,
            gender="none",
            role=req.role,
        )
        return await self.users_repository.create(user)

    async def list_users(self) -> list[User]:
        return await self.users_repository.list_all()
