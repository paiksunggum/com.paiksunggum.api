"""Windows용 uvicorn loop factory — psycopg async는 ProactorEventLoop를 쓸 수 없다."""

from __future__ import annotations

import asyncio
import selectors
import sys


def selector_loop_factory(use_subprocess: bool = False) -> asyncio.AbstractEventLoop:
    """uvicorn custom loop: 한 번 호출되어 event loop 인스턴스를 반환한다."""
    del use_subprocess
    if sys.platform == "win32":
        return asyncio.SelectorEventLoop(selectors.SelectSelector())
    return asyncio.SelectorEventLoop()
