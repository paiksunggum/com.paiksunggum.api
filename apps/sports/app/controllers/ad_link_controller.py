from sqlalchemy.ext.asyncio import AsyncSession

from ..schemas.ad_link_schema import AdExposureCreateRequest
from ..services.ad_link_service import AdLinkService


class AdLinkController:
    def __init__(self, session: AsyncSession) -> None:
        self.service = AdLinkService(session)

    async def record_exposure(self, video_id: int, req: AdExposureCreateRequest):
        return await self.service.record_exposure(video_id, req)
