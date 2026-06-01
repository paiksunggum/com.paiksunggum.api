from abc import ABC, abstractmethod
from typing import TypedDict


class SignupResult(TypedDict):
    id: int
    user_id: str
    email: str
    name: str
    birthdate: str
    gender: str
    role: str


class SignupRepository(ABC):
    @abstractmethod
    async def exists_by_login_id(login_id: str) -> bool:
        ...

    @abstractmethod
    async def create(
        login_id: str,
        password_hash: str,
        email: str,
        name: str,
        birthdate: str,
        gender: str,
        role: str,
    ) -> SignupResult:
        ...
