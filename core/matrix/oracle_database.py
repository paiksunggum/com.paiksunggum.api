"""Backward-compatible import path for database_manager."""

from core.matrix.database_manager import (
    AsyncSessionLocal,
    Base,
    create_all_tables,
    dispose_engine,
    engine,
    get_db,
    init_engine,
    neon_now,
    normalize_async_database_url,
)

__all__ = [
    "AsyncSessionLocal",
    "Base",
    "create_all_tables",
    "dispose_engine",
    "engine",
    "get_db",
    "init_engine",
    "neon_now",
    "normalize_async_database_url",
]
