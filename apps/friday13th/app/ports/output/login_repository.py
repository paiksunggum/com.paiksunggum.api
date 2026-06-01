from abc import ABC, abstractmethod


class LoginRepository(ABC):
    @abstractmethod
    async def find_by_login_id(login_id: str) -> str | None:
        """계정이 있으면 password_hash, 없으면 None."""
        ...

    @abstractmethod
    async def find_by_email(email: str) -> str | None:
        """계정이 있으면 password_hash, 없으면 None."""
        ...
