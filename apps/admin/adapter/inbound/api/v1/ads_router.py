from fastapi import APIRouter, Depends

from apps.admin.adapter.inbound.api.schemas.ads_schema import AdsSchema
from apps.admin.app.dtos.ads_dto import AdsResponse
from apps.admin.app.ports.input.ads_use_case import AdsUseCase
from apps.admin.dependencies.ads_provider import get_ads_use_case

'''
스털링 광고 국장 — 광고·상품 메타데이터
'''

ads_router = APIRouter(prefix="/admin/ads", tags=["ads"])


@ads_router.get("/myself")
async def introduce_myself(
    ads: AdsUseCase = Depends(get_ads_use_case),
) -> AdsResponse:
    return await ads.introduce_myself(
        AdsSchema(
            id=3,
            name="Ads"
        )
    )

