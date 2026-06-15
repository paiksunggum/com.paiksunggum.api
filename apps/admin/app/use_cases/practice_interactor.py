from __future__ import annotations

import logging

from apps.admin.adapter.inbound.api.schemas.practice_schema import PracticeSchema
from apps.admin.app.dtos.practice_dto import PracticeQuery, PracticeResponse
from apps.admin.app.ports.input.practice_use_case import PracticeUseCase
from apps.admin.app.ports.output.practice_repository import PracticeRepository


class PracticeInteractor(PracticeUseCase):

    def __init__(self, repository: PracticeRepository):
        self.repository = repository

    async def introduce_myself(self, schema: PracticeSchema) -> PracticeResponse:
        '''practice 의 자기소개 인터렉트'''

        return await self.repository.introduce_myself(PracticeQuery(
            sports_id = schema.sports_id,
            title = schema.title,
            description = schema.description,
            guide_json = schema.guide_json,
            is_active = schema.is_active,
        ))
