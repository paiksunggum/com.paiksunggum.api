from fastapi import APIRouter

from apps.automode.adapter.inbound.api.v1.email_router import email_router

automode_router = APIRouter(prefix="/api/automode", tags=["automode"])
automode_router.include_router(email_router)

__all__ = ["automode_router"]
