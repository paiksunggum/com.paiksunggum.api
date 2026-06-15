from fastapi import APIRouter, Depends

from apps.admin.adapter.inbound.api.schemas.sports_schema import SportsSchema
from apps.admin.app.dtos.sports_dto import SportsResponse
from apps.admin.app.ports.input.sports_use_case import SportsUseCase
from apps.admin.dependencies.sports_provider import get_sports_use_case

'''
해리스 국장 — 스포츠 종목 마스터
'''

sports_router = APIRouter(prefix="/admin/sports", tags=["sports"])


@sports_router.get("/myself")
async def introduce_myself(
    sports: SportsUseCase = Depends(get_sports_use_case),
) -> SportsResponse:
    return await sports.introduce_myself(
        SportsSchema(
            id=1,
            name="Sports"
        )
    )
