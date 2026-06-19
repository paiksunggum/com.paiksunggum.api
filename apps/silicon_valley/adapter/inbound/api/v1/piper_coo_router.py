import logging

from fastapi import APIRouter, Depends

from apps.silicon_valley.adapter.inbound.api.schemas.piper_coo_schema import (
    PiperCooResponseSchema,
    PiperCooSchema,
)
from apps.silicon_valley.app.ports.input.piper_coo_use_case import PiperCooUseCase
from apps.silicon_valley.dependencies.piper_coo_provider import get_piper_coo_use_case

logger = logging.getLogger("apps")
piper_coo_router = APIRouter(prefix="/coo", tags=["piper-coo"])


@piper_coo_router.get("/myself", response_model=PiperCooResponseSchema)
async def introduce_myself(
    piper: PiperCooUseCase = Depends(get_piper_coo_use_case),
) -> PiperCooResponseSchema:
    result = await piper.introduce_myself(PiperCooSchema(id=2, name="Jared Dunn"))
    return PiperCooResponseSchema(id=result.id, name=result.name)
