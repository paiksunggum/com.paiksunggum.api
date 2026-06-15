from __future__ import annotations

import logging

from apps.admin.adapter.inbound.api.schemas.users_ad_schema import UsersAdSchema
from apps.admin.app.dtos.users_ad_dto import UsersAdQuery, UsersAdResponse
from apps.admin.app.ports.input.users_ad_use_case import UsersAdUseCase
from apps.admin.app.ports.output.users_ad_repository import UsersAdRepository


class UsersAdInteractor(UsersAdUseCase):

    def __init__(self, repository: UsersAdRepository):
        self.repository = repository

    async def introduce_myself(self, schema: UsersAdSchema) -> UsersAdResponse:
        '''users_ad 의 자기소개 인터렉트'''

        return await self.repository.introduce_myself(UsersAdQuery(
            user_id = schema.user_id,
            ad_id = schema.ad_id,
            contract_status = schema.contract_status,
            allocated_budget = schema.allocated_budget,
            started_at = schema.started_at,
            ended_at = schema.ended_at,
        ))
