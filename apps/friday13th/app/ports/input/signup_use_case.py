from abc import ABC, abstractmethod

from ..output.signup_repository import SignupResult


class SignupUseCase(ABC):
    @abstractmethod
    async def signup(
        user_id: str,
        password: str,
        email: str,
        name: str,
        birthdate: str,
        gender: str,
        role: str,
    ) -> SignupResult:
        """회원가입 성공 시 생성된 사용자 정보. 실패 시 ValueError."""
        ...
