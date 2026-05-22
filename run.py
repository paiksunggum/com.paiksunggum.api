"""로컬 개발 서버 실행: python run.py (backend 폴더에서)."""

import uvicorn

if __name__ == "__main__":
    uvicorn.run(
        "apps.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
    )
