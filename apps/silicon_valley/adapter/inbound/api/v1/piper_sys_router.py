import logging

from fastapi import APIRouter, Depends

from apps.silicon_valley.adapter.inbound.api.schemas.piper_sys_schema import (
    PiperSysResponseSchema,
    PiperSysSchema,
)
from apps.silicon_valley.app.ports.input.piper_sys_use_case import PiperSysUseCase
from apps.silicon_valley.dependencies.piper_sys_provider import get_piper_sys_use_case

logger = logging.getLogger("apps")
piper_sys_router = APIRouter(prefix="/sys", tags=["piper-sys"])


@piper_sys_router.get("/myself", response_model=PiperSysResponseSchema)
async def introduce_myself(
    piper: PiperSysUseCase = Depends(get_piper_sys_use_case),
) -> PiperSysResponseSchema:
    result = await piper.introduce_myself(PiperSysSchema(id=5, name="Bertram Gilfoyle"))
    return PiperSysResponseSchema(id=result.id, name=result.name)
