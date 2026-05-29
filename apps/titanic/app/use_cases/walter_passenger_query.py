import logging

from sqlalchemy.ext.asyncio import AsyncSession

from ..ports.input.walter_query_use_case import WalterQueryUseCase
from ..ports.output.walter_repository import WalterPassengerPage, WalterRepository

logger = logging.getLogger("apps")


class WalterPassengerQuery(WalterQueryUseCase):
    """라우터에서 받은 조회 요청을 출력 포트(리포지토리)로 전달한다."""

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
            "[유스케이스→저장소] WalterPassengerQuery → %s | page=%d, page_size=%d",
            type(self._repository).__name__,
            safe_page,
            safe_page_size,
        )
        return await self._repository.get_passengers(
            page=safe_page,
            page_size=safe_page_size,
            db=db,
        )
