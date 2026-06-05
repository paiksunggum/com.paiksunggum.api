from sqlalchemy.ext.asyncio import AsyncSession

from ..models.users_ad_model import UsersAd
from ..repositories.users_ad_repository import UsersAdRepository
from ..schemas.users_ad_schema import UsersAdNestedCreateRequest


class UsersAdService:
    def __init__(self, session: AsyncSession) -> None:
        self.repository = UsersAdRepository(session)

    async def create_contract(
        self, user_id: int, req: UsersAdNestedCreateRequest
    ) -> UsersAd:
        row = UsersAd(
            user_id=user_id,
            ad_id=req.ad_id,
            contract_status=req.contract_status,
            allocated_budget=req.allocated_budget,
            ended_at=req.ended_at,
        )
        if req.started_at is not None:
            row.started_at = req.started_at
        return await self.repository.create(row)
