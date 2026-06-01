import logging
from typing import Any

from ..ports.input.james_command_use_case import JamesCommandUseCase
from ..ports.output.james_repository import JamesRepository

logger = logging.getLogger("apps")


class JamesCommandInteractor(JamesCommandUseCase):
    """라우터에서 받은 승객 레코드를 출력 포트(리포지토리)로 전달한다."""

    def __init__(self, repository: JamesRepository) -> None:
        self._repository = repository

    async def upload_passengers(
        self,
        records: list[dict[str, Any]],
    ) -> dict[str, Any]:
        logger.info(
            "[유스케이스→저장소] JamesCommand → %s | 승객 %d행 전달",
            type(self._repository).__name__,
            len(records),
        )
        return await self._repository.upload_passengers(records)
