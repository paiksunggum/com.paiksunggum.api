from abc import ABC, abstractmethod
from typing import TypedDict

from sqlalchemy.ext.asyncio import AsyncSession


class WalterPassengerItem(TypedDict):
    id: int
    passengerId: str
    name: str
    gender: str
    age: str
    pclass: str
    survived: str


class WalterPassengerPage(TypedDict):
    page: int
    pageSize: int
    total: int
    totalPages: int
    items: list[WalterPassengerItem]


class WalterRepository(ABC):
    @abstractmethod
    async def get_passengers(
        page: int,
        page_size: int,
        db: AsyncSession,
    ) -> WalterPassengerPage:
        ...
