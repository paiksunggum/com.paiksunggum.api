import logging

from ..ports.input.signup_use_case import SignupUseCase
from ..ports.output.signup_repository import SignupRepository, SignupResult
from ..security import hash_password

logger = logging.getLogger("apps")


class SignupInteractor(SignupUseCase):
    def __init__(self, repository: SignupRepository) -> None:
        self._repository = repository

    async def signup(
        self,
        user_id: str,
        password: str,
        email: str,
        name: str,
        birthdate: str,
        gender: str,
        role: str,
    ) -> SignupResult:
        resolved_email = email.strip() if email.strip() else f"{user_id}@naver.com"
        logger.info(
            "[유스케이스→저장소] SignupInteractor → %s | user_id=%s email=%s",
            type(self._repository).__name__,
            user_id,
            resolved_email,
        )
        if await self._repository.exists_by_login_id(user_id):
            raise ValueError("이미 사용 중인 아이디입니다.")

        role_str = role.value if hasattr(role, "value") else str(role)
        return await self._repository.create(
            login_id=user_id,
            password_hash=hash_password(password),
            email=resolved_email,
            name=name,
            birthdate=birthdate,
            gender=gender,
            role=role_str,
        )
