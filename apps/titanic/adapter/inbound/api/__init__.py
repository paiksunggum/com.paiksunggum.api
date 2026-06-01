"""Titanic 인바운드 HTTP 라우터 조립."""

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_db

from apps.titanic.app.ports.input.james_command_use_case import JamesCommandUseCase


def get_james_command_use_case(
    db: AsyncSession = Depends(get_db),
) -> JamesCommandUseCase:
    from apps.titanic.adapter.outbound.pg.walter_pg_repository import JamesPgRepository
    from apps.titanic.app.use_cases.james_command_interactor import JamesCommandInteractor

    return JamesCommandInteractor(JamesPgRepository(db))


from apps.titanic.adapter.inbound.api.v1.james_command_router import james_router
from apps.titanic.adapter.inbound.api.v1.rose_diamond_router import rose_diamond_router
from apps.titanic.adapter.inbound.api.v1.walter_query_router import walter_router

titanic_router = APIRouter()
titanic_router.include_router(james_router)
titanic_router.include_router(rose_diamond_router)
titanic_router.include_router(walter_router)

__all__ = [
    "get_james_command_use_case",
    "james_router",
    "rose_diamond_router",
    "titanic_router",
    "walter_router",
]
