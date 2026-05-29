from typing import Any
import logging

from ...app.ports.output.james_repository import JamesRepository

logger = logging.getLogger("apps")


class InMemoryJamesRepository(JamesRepository):
    """DATABASE_URL 미설정 시 사용하는 인메모리 구현."""

    async def upload_passengers(
        self,
        records: list[dict[str, Any]],
    ) -> dict[str, Any]:
        logger.info("[메모리저장소] 인메모리 저장 | 승객 %d행", len(records))
        return {
            "ok": True,
            "rowCount": len(records),
            "data": records,
            "storedIn": "memory",
        }
