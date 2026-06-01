from abc import ABC, abstractmethod


class LoginUseCase(ABC):
    @abstractmethod
    async def login(login_id: str, password: str) -> None:
        """자격 증명이 맞으면 성공. 실패 시 ValueError."""
        ...
