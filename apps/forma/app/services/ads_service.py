from sqlalchemy.ext.asyncio import AsyncSession

from ..models.ads_model import Ad
from ..repositories.ads_repository import AdsRepository
from ..schemas.ads_schema import AdCreateRequest


class AdsService:
    def __init__(self, session: AsyncSession) -> None:
        self.ads_repository = AdsRepository(session)

    async def create_ad(self, req: AdCreateRequest) -> Ad:
        row = Ad(
            owner_user_id=req.owner_user_id,
            title=req.title,
            product_url=req.product_url,
            image_url=req.image_url,
            status=req.status,
        )
        return await self.ads_repository.create(row)

    async def list_ads(self) -> list[Ad]:
        return await self.ads_repository.list_all()
