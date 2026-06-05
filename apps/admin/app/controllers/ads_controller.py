from sqlalchemy.ext.asyncio import AsyncSession

from ..schemas.ads_schema import AdCreateRequest
from ..services.ads_service import AdsService


class AdsController:
    def __init__(self, session: AsyncSession) -> None:
        self.service = AdsService(session)

    async def create_ad(self, req: AdCreateRequest):
        return await self.service.create_ad(req)

    async def list_ads(self):
        return await self.service.list_ads()
