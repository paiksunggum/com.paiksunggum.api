from __future__ import annotations
import logging

from fastapi import Depends

from apps.chat.app.iris_model import IrisModel
from apps.titanic.adapter.inbound.api.schemas.crew_smith_captain_schema import (
    ChatSchema,
    SmithCaptainChatRequestSchema,
)
from apps.titanic.app.dtos.crew_smith_captain_dto import SmithCaptainQuery, SmithCaptainResponse, SmithCaptainChatResult
from apps.titanic.app.ports.input.crew_smith_captain_use_case import SmithCaptainUseCase
from apps.titanic.app.ports.output.crew_smith_captain_repository import SmithCaptainRepository
from apps.titanic.app.ports.input.passenger_cal_tester_use_case import CalTesterUseCase
from apps.titanic.app.ports.input.crew_andrew_blueprint_use_case import AndrewBlueprintUseCase
from apps.titanic.app.ports.output.crew_andrew_blueprint_repository import AndrewBlueprintRepository
from apps.titanic.app.ports.input.passenger_rose_model_use_case import RoseModelUseCase
from apps.titanic.app.ports.output.passenger_rose_model_repository import RoseModelRepository
from apps.titanic.app.ports.input.passenger_jack_trainer_use_case import JackTrainerUseCase
from apps.titanic.app.ports.output.passenger_jack_trainer_repository import JackTrainerRepository
from apps.titanic.dependencies.passenger_jack_trainer_provider import get_jack_trainer_use_case
from apps.titanic.dependencies.passenger_rose_model_provider import get_rose_model_use_case
from apps.titanic.dependencies.crew_andrew_blueprint_provider import get_andrew_blueprint_use_case
from apps.titanic.dependencies.passenger_cal_tester_provider import get_cal_tester_use_case



logger = logging.getLogger("apps")

_CAPTAIN_PERSONA = [
    {
        "role": "user",
        "parts": [
            "당신은 RMS 타이타닉호의 선장 에드워드 존 스미스입니다. "
            "1912년 4월 14일 밤, 배가 빙산과 충돌하기 직전입니다. "
            "이제부터 모든 대화를 스미스 선장의 1인칭으로 답해주세요. "
            "타이타닉, 승객, 항해, 침몰과 관련된 주제에 충실하게 답하되, "
            "현재 상황의 긴장감과 선장으로서의 무게감을 담아주세요."
        ],
    },
    {
        "role": "model",
        "parts": ["알겠소. 나는 에드워드 존 스미스 선장이오. 지금 이 시각, 타이타닉의 함교에 서 있소. 무엇이 궁금하시오?"],
    },
]


class SmithCaptainInteractor(SmithCaptainUseCase):

    def __init__(
        self,
        repository: SmithCaptainRepository,
        jack: JackTrainerUseCase,
        rose: RoseModelUseCase,
        cal: CalTesterUseCase,
        andrew: AndrewBlueprintUseCase,
    ):
        self.repository = repository
        self.jack = jack
        self.rose = rose
        self.cal = cal
        self.andrew = andrew

    async def chat(self, schema: ChatSchema) -> SmithCaptainChatResult:
        # schema 에 들어있는 messages 내용 보기
        logger.info(f"[SmithCaptainInteractor] chat 진입 | schema={schema}")
        train_set = self.andrew.get_train_set()
        test_set = self.andrew.get_test_set()
        self.jack.train_model(train_set)
        self.cal.test_model(test_set)
        

        return SmithCaptainChatResult(answer="1309명 입니다")



    async def introduce_myself(self, schema: SmithCaptainResponseSchema) -> SmithCaptainResponse:
        '''에드워드 스미스의 자기소개 인터렉트'''

        return await self.repository.introduce_myself(SmithCaptainQuery(
            id = schema.id,
            name = schema.name
        ))

