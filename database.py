"""Neon(PostgreSQL) 비동기 SQLAlchemy 연결 — FastAPI DI용."""

from __future__ import annotations

import os
from collections.abc import AsyncGenerator
from pathlib import Path

from dotenv import load_dotenv
from sqlalchemy import text
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import DeclarativeBase

_backend_dir = Path(__file__).resolve().parent
load_dotenv(_backend_dir / ".env")

engine: AsyncEngine | None = None
AsyncSessionLocal: async_sessionmaker[AsyncSession] | None = None


class Base(DeclarativeBase):
    pass


def normalize_async_database_url(url: str) -> str:
    """Neon/일반 postgres URL을 SQLAlchemy asyncio + psycopg3 형식으로 맞춘다."""
    u = url.strip()
    if not u:
        raise ValueError("DATABASE_URL is not set")
    if "+psycopg_async" in u:
        return u
    if u.startswith("postgresql+psycopg://"):
        return u.replace("postgresql+psycopg://", "postgresql+psycopg_async://", 1)
    if u.startswith("postgresql://"):
        return u.replace("postgresql://", "postgresql+psycopg_async://", 1)
    if u.startswith("postgres://"):
        return u.replace("postgres://", "postgresql+psycopg_async://", 1)
    raise ValueError(
        "DATABASE_URL must start with postgresql://, postgres://, or postgresql+psycopg://"
    )


def _init_engine() -> None:
    global engine, AsyncSessionLocal
    raw = (os.getenv("DATABASE_URL") or "").strip()
    if not raw:
        return
    engine = create_async_engine(normalize_async_database_url(raw), echo=False)
    AsyncSessionLocal = async_sessionmaker(engine, expire_on_commit=False)


_init_engine()


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    if AsyncSessionLocal is None:
        raise RuntimeError("DATABASE_URL is not set")
    async with AsyncSessionLocal() as session:
        yield session


async def create_tables() -> None:
    if engine is None:
        return

    from apps.friday13th.app.models.user import User  # noqa: F401
    from apps.titanic.adapter.outbound.pg.james_pg_repository import (  # noqa: F401
        TitanicPassengerModel,
    )
    from sqlmodel import SQLModel

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        await conn.run_sync(SQLModel.metadata.create_all)


async def neon_now(db: AsyncSession) -> dict[str, str]:
    result = await db.execute(text("SELECT NOW() AS now"))
    return {"now": str(result.scalar_one())}
