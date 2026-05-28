from typing import Any
import logging

from ..ports.output.james_repository import JamesRepository

logger = logging.getLogger("apps")


class JamesCommand:
    """입력 포트에서 전달받은 업로드 데이터를 출력 포트(리포지토리)로 전달한다."""

    def __init__(self, repository: JamesRepository) -> None:
        self._repository = repository

    async def upload_passengers(
        self,
        *,
        file_name: str,
        columns: list[str],
        rows: list[dict[str, str]],
    ) -> dict[str, Any]:
        logger.info(
            "[JamesCommand] call repository - file=%s, repository=%s, rows=%d",
            file_name,
            type(self._repository).__name__,
            len(rows),
        )
        result = await self._repository.save_uploaded_passengers(
            file_name=file_name,
            columns=columns,
            rows=rows,
        )
        logger.info(
            "[JamesCommand] repository returned - file=%s, stored_in=%s, rows=%s",
            file_name,
            result.get("storedIn"),
            result.get("rowCount"),
        )
        return result
