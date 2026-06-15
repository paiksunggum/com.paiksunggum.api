from fastapi import APIRouter, Depends

from apps.admin.adapter.inbound.api.schemas.users_ad_schema import UsersAdSchema
from apps.admin.app.dtos.users_ad_dto import UsersAdResponse
from apps.admin.app.ports.input.users_ad_use_case import UsersAdUseCase
from apps.admin.dependencies.users_ad_provider import get_users_ad_use_case

'''
모건 어카운트 매니저 — 유저별 광고 계약·집행
'''

users_ad_router = APIRouter(prefix="/admin/users-ad", tags=["users-ad"])


@users_ad_router.get("/myself")
async def introduce_myself(
    users_ad: UsersAdUseCase = Depends(get_users_ad_use_case),
) -> UsersAdResponse:
    return await users_ad.introduce_myself(
        UsersAdSchema(
            id=4,
            name="Users_Ad"
        )
    )



