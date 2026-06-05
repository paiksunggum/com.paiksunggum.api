"""Titanic 인바운드 HTTP 라우터 조립."""

from fastapi import APIRouter

from apps.titanic.adapter.inbound.api.v1.andrew_blueprint_router import andrew_blueprint_router
from apps.titanic.adapter.inbound.api.v1.james_command_router import james_router
from apps.titanic.adapter.inbound.api.v1.rose_diamond_router import rose_diamond_router

titanic_router = APIRouter()
titanic_router.include_router(james_router)
titanic_router.include_router(rose_diamond_router)
titanic_router.include_router(andrew_blueprint_router)

__all__ = [
    "andrew_blueprint_router",
    "james_router",
    "rose_diamond_router",
    "titanic_router",
]
