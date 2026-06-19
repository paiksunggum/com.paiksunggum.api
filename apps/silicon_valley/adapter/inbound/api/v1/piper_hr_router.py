import logging

from fastapi import APIRouter, Depends

from apps.silicon_valley.adapter.inbound.api.schemas.piper_hr_schema import (
    PiperHrResponseSchema,
    PiperHrSchema,
)
from apps.silicon_valley.app.ports.input.piper_hr_use_case import PiperHrUseCase
from apps.silicon_valley.dependencies.piper_hr_provider import get_piper_hr_use_case

logger = logging.getLogger("apps")
piper_hr_router = APIRouter(prefix="/hr", tags=["piper-hr"])


@piper_hr_router.get("/myself", response_model=PiperHrResponseSchema)
async def introduce_myself(
    piper: PiperHrUseCase = Depends(get_piper_hr_use_case),
) -> PiperHrResponseSchema:
    result = await piper.introduce_myself(PiperHrSchema(id=4, name="HR Manager"))
    return PiperHrResponseSchema(id=result.id, name=result.name)
