from sqlalchemy.ext.asyncio import AsyncSession

from ..models.ad_link_model import AdLink
from ..repositories.ad_link_repository import AdLinkRepository
from ..schemas.ad_link_schema import AdExposureCreateRequest


class AdLinkService:
    def __init__(self, session: AsyncSession) -> None:
        self.ad_link_repository = AdLinkRepository(session)

    async def record_exposure(
        self, video_id: int, req: AdExposureCreateRequest
    ) -> AdLink:
        row = AdLink(
            video_id=video_id,
            ad_id=req.ad_id,
            placement_type=req.placement_type,
        )
        if req.exposed_at is not None:
            row.exposed_at = req.exposed_at
        return await self.ad_link_repository.create(row)
