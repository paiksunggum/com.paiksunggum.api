import logging

from sqlalchemy.ext.asyncio import AsyncSession

from ..ports.output.walter_repository import WalterPassengerPage, WalterRepository

logger = logging.getLogger("apps")


class WalterPassengerQuery:
    def __init__(self, repository: WalterRepository) -> None:
        self._repository = repository

    async def get_passengers(
        self,
        *,
        page: int,
        page_size: int,
        db: AsyncSession,
    ) -> WalterPassengerPage:
        safe_page = max(page, 1)
        safe_page_size = min(max(page_size, 1), 100)
        logger.info(
            "[WalterPassengerQuery] call repository - page=%d, page_size=%d",
            safe_page,
            safe_page_size,
        )
        result = await self._repository.read_passengers(
            page=safe_page,
            page_size=safe_page_size,
            db=db,
        )
        logger.info(
            "[WalterPassengerQuery] repository returned - total=%d, returned=%d",
            result["total"],
            len(result["items"]),
        )
        return result
