from __future__ import annotations
import logging

from apps.titanic.adapter.inbound.api.schemas.passenger_cal_tester_schema import CalTesterSchema
from apps.titanic.app.dtos.passenger_cal_tester_dto import CalTesterQuery, CalTesterResponse
from apps.titanic.app.ports.input.passenger_cal_tester_use_case import CalTesterUseCase
from apps.titanic.app.ports.output.passenger_cal_tester_repository import CalTestRepository

logger = logging.getLogger("apps")

class CalTesterInteractor(CalTesterUseCase):
    
    def __init__(self, repository: CalTestRepository):
        self.repository = repository

    async def introduce_myself(self, schema: CalTesterSchema) -> CalTesterResponse:
        '''칼 헉클리의 자기소개 인터렉트'''
        
        return await self.repository.introduce_myself(CalTesterQuery(
            id = schema.id,
            name = schema.name
        ))