from __future__ import annotations

import logging

logger = logging.getLogger(__name__)
from sqlalchemy.ext.asyncio import AsyncSession

from apps.admin.app.dtos.users_ad_dto import UsersAdQuery, UsersAdResponse
from apps.admin.app.ports.output.users_ad_repository import UsersAdRepository


class UsersAdPgRepository(UsersAdRepository):
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def introduce_myself(self, query: UsersAdQuery) -> UsersAdResponse:

        '''users_ad 의 자기 소개 레포지토리 구현 메소드'''

        logger.info(f"[UsersAdPgRepository] introduce_myself 진입 | request_data={query}")

        response: UsersAdResponse = UsersAdResponse(
            id=query.user_id * 10000,
            user_id=query.user_id,
            ad_id=query.ad_id,
            contract_status=query.contract_status + "가 레포지토리에 다녀옴",
            allocated_budget=query.allocated_budget,
            started_at=query.started_at,
            ended_at=query.ended_at,
            created_at=None,
        )
        return response
