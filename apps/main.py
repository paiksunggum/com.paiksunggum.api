import logging
import os
import sys

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.exc import OperationalError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from sqlalchemy.ext.asyncio import AsyncSession


def _configure_app_logging() -> None:
    """uvicorn 접근 로그와 별도로 apps.* logger.info 를 터미널에 출력한다."""
    log = logging.getLogger("apps")
    log.setLevel(logging.INFO)
    if log.handlers:
        return
    handler = logging.StreamHandler(sys.stderr)
    handler.setFormatter(logging.Formatter("%(levelname)s:     %(message)s"))
    log.addHandler(handler)


_configure_app_logging()

from .matrix.app.keymaker import get_keymaker

keymaker = get_keymaker()

from .friday13th.adapter.inbound.api.schemas import InitDbResponse
from .friday13th.adapter.inbound.api.v1.login_router import login_router
from .friday13th.adapter.inbound.api.v1.signup_router import signup_router
from .chat.app.chat_page import chat_page_html
from .home_page import home_page_html
from .chat.app.chloe_controller import ChloeController
from .chat.app.schemas import ChatRequest, ChatResponse
from .database import create_tables, get_db, neon_now
from .forma.app.forma_routes import router as forma_router
from .titanic.adapter.inbound.api import titanic_router
from .weather.app.schemas import WeatherResponse
from .weather.app.weather_controller import WeatherController


_docs_enabled = os.getenv("ENABLE_API_DOCS", "").lower() in ("1", "true", "yes")

app = FastAPI(
    title="TJ Watson Main Page",
    docs_url="/docs" if _docs_enabled else None,
    redoc_url="/redoc" if _docs_enabled else None,
    openapi_url="/openapi.json" if _docs_enabled else None,
    swagger_ui_parameters={"operationsSorter": "method"},
)

app.include_router(forma_router)
app.include_router(titanic_router)
app.include_router(login_router)
app.include_router(signup_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def on_startup() -> None:
    await create_tables()


@app.get("/", response_class=HTMLResponse)
def read_root():
    return home_page_html()


@app.get("/db-check")
async def check_db(db: AsyncSession = Depends(get_db)):
    return await neon_now(db)


@app.get("/weather/current", response_model=WeatherResponse)
async def weather_current(
    city: str = "Seoul",
    lat: float | None = None,
    lon: float | None = None,
):
    try:
        return await WeatherController().get_current(
            city=city if lat is None or lon is None else None,
            lat=lat,
            lon=lon,
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e
    except Exception as e:
        raise HTTPException(
            status_code=502,
            detail=f"날씨 정보를 가져오지 못했습니다: {e}",
        ) from e


@app.get("/chat", response_class=HTMLResponse)
def chat_page():
    return chat_page_html()


@app.post("/chat", response_model=ChatResponse)
def chat(req: ChatRequest):
    try:
        return ChloeController().chat(req)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e
    except Exception as e:
        raise HTTPException(
            status_code=502,
            detail=f"Gemini 응답 생성에 실패했습니다: {e}",
        ) from e


@app.post("/secom/db/init", response_model=InitDbResponse)
async def secom_init_db():
    await create_tables()
    return InitDbResponse(
        ok=True,
        message="users 테이블을 준비했습니다.",
        seeded=[],
    )


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "apps.main:app",
        host="127.0.0.1",
        port=8000,
        reload=True,
        reload_dirs=["apps"],
    )
