import logging

from fastapi import APIRouter, Depends

from apps.silicon_valley.adapter.inbound.api.schemas.piper_ceo_schema import (
    PiperCeoResponseSchema,
    PiperCeoSchema,
)
from apps.silicon_valley.app.ports.input.piper_ceo_use_case import PiperCeoUseCase
from apps.silicon_valley.dependencies.piper_ceo_provider import get_piper_ceo_use_case

logger = logging.getLogger("apps")
piper_ceo_router = APIRouter(prefix="/ceo", tags=["piper-ceo"])


@piper_ceo_router.get("/myself", response_model=PiperCeoResponseSchema)
async def introduce_myself(
    piper: PiperCeoUseCase = Depends(get_piper_ceo_use_case),
) -> PiperCeoResponseSchema:
    result = await piper.introduce_myself(PiperCeoSchema(id=1, name="Richard Hendricks"))
    return PiperCeoResponseSchema(id=result.id, name=result.name)
