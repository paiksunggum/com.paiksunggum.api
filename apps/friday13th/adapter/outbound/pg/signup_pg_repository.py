from datetime import date

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError, OperationalError
from sqlalchemy.ext.asyncio import AsyncSession

from apps.friday13th.adapter.outbound.orm.user import User
from apps.friday13th.app.ports.output.signup_repository import SignupRepository, SignupResult


def _parse_birthdate(value: str) -> date:
    if len(value) == 8 and value.isdigit():
        return date(int(value[:4]), int(value[4:6]), int(value[6:8]))
    return date.fromisoformat(value)


class SignupPgRepository(SignupRepository):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def exists_by_login_id(self, login_id: str) -> bool:
        try:
            result = await self._session.execute(
                select(User).where(User.login_id == login_id)
            )
            return result.scalar_one_or_none() is not None
        except OperationalError as e:
            raise RuntimeError(
                "데이터베이스 연결에 실패했습니다. 잠시 후 다시 시도해 주세요."
            ) from e

    async def create(
        self,
        login_id: str,
        password_hash: str,
        email: str,
        name: str,
        birthdate: str,
        gender: str,
        role: str,
    ) -> SignupResult:
        user = User(
            login_id=login_id,
            password_hash=password_hash,
            email=email,
            name=name,
            birthdate=_parse_birthdate(birthdate).strftime("%Y%m%d"),
            gender=gender,
            role=role,
        )
        try:
            self._session.add(user)
            await self._session.commit()
            await self._session.refresh(user)
        except IntegrityError as e:
            raise ValueError("이미 사용 중인 아이디입니다.") from e
        except OperationalError as e:
            raise RuntimeError(
                "데이터베이스 연결에 실패했습니다. 잠시 후 다시 시도해 주세요."
            ) from e
        return SignupResult(
            id=user.id,
            user_id=user.login_id,
            email=user.email,
            name=user.name,
            birthdate=user.birthdate,
            gender=user.gender,
            role=user.role,
        )
