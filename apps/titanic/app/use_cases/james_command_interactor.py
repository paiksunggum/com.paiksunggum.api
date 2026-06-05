import logging
from typing import Any

from ...adapter.inbound.api.schemas.james_command_schema import JamesCommandSchema
from ..ports.input.james_command_use_case import JamesCommandUseCase
from ..ports.output.james_repository import JamesRepository

logger = logging.getLogger("apps")


class JamesCommandInteractor(JamesCommandUseCase):
    """라우터에서 받은 승객 레코드를 출력 포트(리포지토리)로 전달한다."""

    def __init__(self, repository: JamesRepository) -> None:
        self._repository = repository

    async def upload_passengers(
        self,
        passengers: list[JamesCommandSchema],
    ) -> dict[str, Any]:
        """JamesCommandUseCase.upload_passengers (강의 receive_uploaded_records 대응)."""
        logger.info("[제임스 유스케이스] 스키마로 변환된 상위 5개 레코드 예시")
        for record in passengers[:5]:
            logger.info("%s", record.model_dump(by_alias=True))

        records = [p.model_dump(by_alias=True) for p in passengers]
        return await self._repository.upload_passengers(records)
