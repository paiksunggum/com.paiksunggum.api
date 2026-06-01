import logging

from ..ports.input.login_use_case import LoginUseCase
from ..ports.output.login_repository import LoginRepository
from ..security import verify_password

logger = logging.getLogger("apps")


class LoginInteractor(LoginUseCase):
    def __init__(self, repository: LoginRepository) -> None:
        self._repository = repository

    async def login(self, login_id: str, password: str) -> None:
        logger.info(
            "[유스케이스→저장소] LoginInteractor → %s | login_id=%s",
            type(self._repository).__name__,
            login_id,
        )
        stored = await self._repository.find_by_login_id(login_id)
        if stored is None:
            stored = await self._repository.find_by_email(login_id)
        if stored is None or not verify_password(password, stored):
            raise ValueError("아이디 또는 비밀번호가 올바르지 않습니다.")
