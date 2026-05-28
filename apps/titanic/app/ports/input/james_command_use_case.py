from typing import Any, Protocol
import logging

from ...use_cases.james_command import JamesCommand

logger = logging.getLogger("apps")


class JamesCommandUseCase(Protocol):
    async def upload_passengers(
        self,
        *,
        file_name: str,
        columns: list[str],
        rows: list[dict[str, str]],
    ) -> dict[str, Any]:
        ...


class JamesCommandUseCaseImpl:
    """라우터 → 유스케이스 → 리포지토리(어댑터) 연결."""

    def __init__(self, james_command: JamesCommand) -> None:
        self._james_command = james_command

    async def upload_passengers(
        self,
        *,
        file_name: str,
        columns: list[str],
        rows: list[dict[str, str]],
    ) -> dict[str, Any]:
        logger.info(
            "[JamesCommandUseCase] dispatch - file=%s, rows=%d",
            file_name,
            len(rows),
        )
        result = await self._james_command.upload_passengers(
            file_name=file_name,
            columns=columns,
            rows=rows,
        )
        logger.info(
            "[JamesCommandUseCase] complete - file=%s, stored_in=%s, rows=%s",
            file_name,
            result.get("storedIn"),
            result.get("rowCount"),
        )
        return result
