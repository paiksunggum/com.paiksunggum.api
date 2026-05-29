from abc import ABC, abstractmethod

from sqlalchemy.ext.asyncio import AsyncSession

from ..output.walter_repository import WalterPassengerPage


class WalterQueryUseCase(ABC):
    @abstractmethod
    async def get_passengers(
        page: int,
        page_size: int,
        db: AsyncSession,
    ) -> WalterPassengerPage:
        ...
