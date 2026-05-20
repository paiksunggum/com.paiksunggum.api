from sqlalchemy.ext.asyncio import AsyncSession

from ..models.ad_link_model import AdLink
from ..repositories.ad_link_repository import AdLinkRepository
from ..schemas.ad_link_schema import AdLinkCreateRequest


class AdLinkService:
    def __init__(self, session: AsyncSession) -> None:
        self.ad_link_repository = AdLinkRepository(session)

    async def create_ad_link(self, req: AdLinkCreateRequest) -> AdLink:
        row = AdLink(
            video_id=req.video_id,
            ad_id=req.ad_id,
            placement_type=req.placement_type,
            start_sec=req.start_sec,
            end_sec=req.end_sec,
        )
        return await self.ad_link_repository.create(row)

    async def list_ad_links(self) -> list[AdLink]:
        return await self.ad_link_repository.list_all()
