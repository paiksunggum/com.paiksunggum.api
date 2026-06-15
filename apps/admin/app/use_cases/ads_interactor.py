from __future__ import annotations

import logging

from apps.admin.adapter.inbound.api.schemas.ads_schema import AdsSchema
from apps.admin.app.dtos.ads_dto import AdsQuery, AdsResponse
from apps.admin.app.ports.input.ads_use_case import AdsUseCase
from apps.admin.app.ports.output.ads_repository import AdsRepository


class AdsInteractor(AdsUseCase):

    def __init__(self, repository: AdsRepository):
        self.repository = repository

    async def introduce_myself(self, schema: AdsSchema) -> AdsResponse:
        '''ads 의 자기소개 인터렉트'''

        return await self.repository.introduce_myself(AdsQuery(
            title = schema.title,
            image_url = schema.image_url,
            target_url = schema.target_url,
            budget = schema.budget,
            status = schema.status,
        ))
