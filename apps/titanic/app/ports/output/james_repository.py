from typing import Any, Protocol


class JamesRepository(Protocol):
    async def save_uploaded_passengers(
        self,
        *,
        file_name: str,
        columns: list[str],
        rows: list[dict[str, str]],
    ) -> dict[str, Any]:
        ...


class InMemoryJamesRepository:
    """DATABASE_URL 미설정 시 사용하는 인메모리 구현."""

    async def save_uploaded_passengers(
        self,
        *,
        file_name: str,
        columns: list[str],
        rows: list[dict[str, str]],
    ) -> dict[str, Any]:
        return {
            "ok": True,
            "fileName": file_name,
            "rowCount": len(rows),
            "columns": columns,
            "data": rows,
            "storedIn": "memory",
        }
