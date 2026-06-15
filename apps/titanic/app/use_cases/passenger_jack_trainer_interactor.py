from __future__ import annotations
import logging

from kiwipiepy import Kiwi

from apps.titanic.adapter.inbound.api.schemas.passenger_jack_trainer_schema import JackTrainerSchema
from apps.titanic.app.dtos.passenger_jack_trainer_dto import JackTrainerQuery, JackTrainerResponse
from apps.titanic.app.ports.input.passenger_jack_trainer_use_case import JackTrainerUseCase
from apps.titanic.app.ports.output.passenger_jack_trainer_repository import JackTrainerRepository

logger = logging.getLogger("apps")


class JackTrainerInteractor(JackTrainerUseCase):
    
    def __init__(self, repository: JackTrainerRepository):
        self.repository = repository
        # kiwipiepy==0.23.1 이 기능이 주입되는 곳
        self.kiwi = Kiwi()

    async def analyze_message_intent(self, user_message:str) -> dict:
        # 사용자의 질문(message)을 형태소 분석하여 키워드와 의도를 파악한다.
        tokens = self.kiwi.tokenize(user_message)
        keywords = [token.form for token in tokens if token.tag in ("NNG", "NNP", "VV", "VA")]
        return {
            "keywords": keywords,
            "raw_tokens": [(token.form, token.tag) for token in tokens],
        }


    async def introduce_myself(self, schema: JackTrainerSchema) -> JackTrainerResponse:
        '''잭 도슨의 자기소개 인터렉트'''
        
        return await self.repository.introduce_myself(JackTrainerQuery(
            id = schema.id,
            name = schema.name
        ))