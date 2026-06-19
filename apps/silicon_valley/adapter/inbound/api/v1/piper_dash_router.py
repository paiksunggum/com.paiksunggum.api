import logging

from fastapi import APIRouter, Depends

from apps.silicon_valley.adapter.inbound.api.schemas.piper_dash_schema import (
    PiperDashResponseSchema,
    PiperDashSchema,
)
from apps.silicon_valley.app.ports.input.piper_dash_use_case import PiperDashUseCase
from apps.silicon_valley.dependencies.piper_dash_provider import get_piper_dash_use_case

logger = logging.getLogger("apps")
piper_dash_router = APIRouter(prefix="/dash", tags=["piper-dash"])


@piper_dash_router.get("/myself", response_model=PiperDashResponseSchema)
async def introduce_myself(
    piper: PiperDashUseCase = Depends(get_piper_dash_use_case),
) -> PiperDashResponseSchema:
    result = await piper.introduce_myself(PiperDashSchema(id=3, name="Monica Hall"))
    return PiperDashResponseSchema(id=result.id, name=result.name)
