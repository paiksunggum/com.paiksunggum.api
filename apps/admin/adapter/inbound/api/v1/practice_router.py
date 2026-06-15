from fastapi import APIRouter, Depends

from apps.admin.adapter.inbound.api.schemas.practice_schema import PracticeSchema
from apps.admin.app.dtos.practice_dto import PracticeResponse
from apps.admin.app.ports.input.practice_use_case import PracticeUseCase
from apps.admin.dependencies.practice_provider import get_practice_use_case

'''
천 수석 코치 — 종목별 권장 자세 카탈로그
'''

practice_router = APIRouter(prefix="/admin/practice", tags=["practice"])


@practice_router.get("/myself")
async def introduce_myself(
    practice: PracticeUseCase = Depends(get_practice_use_case),
) -> PracticeResponse:
    return await practice.introduce_myself(
        PracticeSchema(
            id=2,
            name="Practice"
        )
    )


