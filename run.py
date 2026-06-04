"""Local dev server.

Usage (from backend/):
    conda activate venv
    python run.py
"""

import os
import sys

import uvicorn

if __name__ == "__main__":
    os.environ["ENABLE_API_DOCS"] = "1"
    # Windows + OneDrive 환경에서는 reload watcher가 Ctrl+C 종료를 늦추는 경우가 있어
    # 기본값은 reload 비활성화로 둔다. 필요 시 RUN_RELOAD=1 로 켠다.
    reload_enabled = os.getenv("RUN_RELOAD", "").lower() in ("1", "true", "yes")
    # uvicorn 0.36+ Windows 기본은 ProactorEventLoop → psycopg async와 충돌
    loop = "loops:selector_loop_factory" if sys.platform == "win32" else "auto"
    uvicorn.run(
        "main:app",
        host="127.0.0.1",
        port=8000,
        loop=loop,
        reload=reload_enabled,
        reload_dirs=[".", "apps"],
    )
