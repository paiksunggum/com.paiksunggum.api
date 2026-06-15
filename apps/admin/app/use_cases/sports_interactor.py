from __future__ import annotations

import logging

from apps.admin.adapter.inbound.api.schemas.sports_schema import SportsSchema
from apps.admin.app.dtos.sports_dto import SportsQuery, SportsResponse
from apps.admin.app.ports.input.sports_use_case import SportsUseCase
from apps.admin.app.ports.output.sports_repository import SportsRepository


class SportsInteractor(SportsUseCase):

    def __init__(self, repository: SportsRepository):
        self.repository = repository

    async def introduce_myself(self, schema: SportsSchema) -> SportsResponse:
        '''sports 의 자기소개 인터렉트'''

        return await self.repository.introduce_myself(SportsQuery(
            name = schema.name,
            description = schema.description,
            is_active = schema.is_active,
        ))
