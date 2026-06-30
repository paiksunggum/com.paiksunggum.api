"""Faker Orchestrator — 지시 전달 전용 오케스트레이터.
SLM(Exaone) 직접 호출 금지. 각 spoke(apps/*)의 outbound 어댑터가 담당한다.
"""

from __future__ import annotations

from collections.abc import Awaitable, Callable
from typing import Any


class FakerOrchestrator:
    """지시만 하는 오케스트레이터. LLM을 직접 호출하지 않는다."""

    def __init__(self) -> None:
        self._tools: dict[str, Callable[..., Awaitable[Any]]] = {}

    def register(self, name: str, handler: Callable[..., Awaitable[Any]]) -> None:
        self._tools[name] = handler

    async def dispatch(self, tool: str, args: dict[str, Any]) -> Any:
        if tool not in self._tools:
            raise ValueError(
                f"알 수 없는 툴: {tool!r}. 사용 가능: {list(self._tools)}"
            )
        return await self._tools[tool](**args)

    @property
    def tool_names(self) -> list[str]:
        return list(self._tools)
