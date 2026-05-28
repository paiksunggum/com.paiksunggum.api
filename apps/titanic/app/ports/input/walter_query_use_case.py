import logging
from typing import Protocol

from sqlalchemy.ext.asyncio import AsyncSession

from ...use_cases.walter_passenger_query import WalterPassengerQuery
from ..output.walter_repository import WalterPassengerPage

logger = logging.getLogger("apps")


class WalterQueryUseCase(Protocol):
    async def get_passengers(
        self,
        *,
        page: int,
        page_size: int,
        db: AsyncSession,
    ) -> WalterPassengerPage:
        ...


class WalterQueryUseCaseImpl:
    def __init__(self, query: WalterPassengerQuery) -> None:
        self._query = query

    async def get_passengers(
        self,
        *,
        page: int,
        page_size: int,
        db: AsyncSession,
    ) -> WalterPassengerPage:
        logger.info(
            "[WalterQueryUseCase] dispatch - page=%d, page_size=%d",
            page,
            page_size,
        )
        result = await self._query.get_passengers(
            page=page,
            page_size=page_size,
            db=db,
        )
        logger.info(
            "[WalterQueryUseCase] complete - total=%d, returned=%d",
            result["total"],
            len(result["items"]),
        )
        return result
