from sqlalchemy.ext.asyncio import AsyncSession

from ..schemas.ad_link_schema import AdLinkCreateRequest
from ..services.ad_link_service import AdLinkService


class AdLinkController:
    def __init__(self, session: AsyncSession) -> None:
        self.service = AdLinkService(session)

    async def create_ad_link(self, req: AdLinkCreateRequest):
        return await self.service.create_ad_link(req)

    async def list_ad_links(self):
        return await self.service.list_ad_links()
