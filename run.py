"""Local dev server.

Usage (from backend/):
    conda activate venv
    python run.py
"""

import os

import uvicorn

if __name__ == "__main__":
    os.environ["ENABLE_API_DOCS"] = "1"
    # reload_dirs limits file watching (StatReload on Windows + OneDrive can hang).
    # watchfiles (requirements) switches reload to WatchFilesReload instead of StatReload.
    uvicorn.run(
        "apps.main:app",
        host="127.0.0.1",
        port=8000,
        reload=True,
        reload_dirs=["apps"],
    )
