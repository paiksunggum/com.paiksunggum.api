"""Silicon Valley 인바운드 HTTP 라우터 조립."""

from fastapi import APIRouter

from apps.silicon_valley.adapter.inbound.api.v1.piper_ceo_router import piper_ceo_router
from apps.silicon_valley.adapter.inbound.api.v1.piper_coo_router import piper_coo_router
from apps.silicon_valley.adapter.inbound.api.v1.piper_dash_router import piper_dash_router
from apps.silicon_valley.adapter.inbound.api.v1.piper_hr_router import piper_hr_router
from apps.silicon_valley.adapter.inbound.api.v1.piper_sys_router import piper_sys_router

silicon_valley_router = APIRouter(prefix="/api/silicon_valley", tags=["silicon-valley"])
silicon_valley_router.include_router(piper_ceo_router)
silicon_valley_router.include_router(piper_coo_router)
silicon_valley_router.include_router(piper_dash_router)
silicon_valley_router.include_router(piper_hr_router)
silicon_valley_router.include_router(piper_sys_router)

__all__ = ["silicon_valley_router"]
