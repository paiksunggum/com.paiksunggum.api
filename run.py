"""로컬 개발 서버 — 사용자가 backend 폴더에서 직접 실행할 때만 사용.

    conda activate venv
    python run.py

에이전트/스크립트가 자동으로 띄우지 않는다. 종료: 터미널에서 Ctrl+C.
"""

import uvicorn

if __name__ == "__main__":
    uvicorn.run(
        "apps.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
    )
