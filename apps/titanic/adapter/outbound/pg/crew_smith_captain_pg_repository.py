from __future__ import annotations

from typing import Any

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from apps.titanic.adapter.outbound.orm.passenger_jack_trainer_orm import JackTrainerORM
from apps.chat.app.iris_model import IrisModel
from apps.titanic.app.dtos.crew_smith_captain_dto import SmithCaptainQuery, SmithCaptainResponse, SmithCaptainChatResult
from apps.titanic.app.ports.output.crew_smith_captain_repository import SmithCaptainRepository

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


class SmithCaptainPgRepository(SmithCaptainRepository):
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def introduce_myself(self, query: SmithCaptainQuery) -> SmithCaptainResponse:
        return SmithCaptainResponse(id=query.id * 10000, name=query.name)

    async def chat(self, message: str) -> SmithCaptainChatResult:
        return SmithCaptainChatResult(answer=message)
