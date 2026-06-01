from sqlalchemy import select
from sqlalchemy.exc import OperationalError
from sqlalchemy.ext.asyncio import AsyncSession

from apps.friday13th.adapter.outbound.orm.user import User
from apps.friday13th.app.ports.output.login_repository import LoginRepository


class LoginPgRepository(LoginRepository):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def find_by_login_id(self, login_id: str) -> str | None:
        try:
            result = await self._session.execute(
                select(User).where(User.login_id == login_id)
            )
            row = result.scalar_one_or_none()
            return row.password_hash if row else None
        except OperationalError as e:
            raise RuntimeError(
                "데이터베이스 연결에 실패했습니다. 잠시 후 다시 시도해 주세요."
            ) from e

    async def find_by_email(self, email: str) -> str | None:
        try:
            result = await self._session.execute(
                select(User).where(User.email == email)
            )
            row = result.scalar_one_or_none()
            return row.password_hash if row else None
        except OperationalError as e:
            raise RuntimeError(
                "데이터베이스 연결에 실패했습니다. 잠시 후 다시 시도해 주세요."
            ) from e
