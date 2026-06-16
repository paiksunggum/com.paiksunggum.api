import logging
from typing import Annotated

from fastapi import APIRouter, Depends, Body
from apps.titanic.adapter.inbound.api.schemas.crew_smith_captain_schema import (
    SmithCaptainResponseSchema,
    ChatSchema,
    SmithCaptainChatRequestSchema,
    SmithCaptainChatResponseSchema,
)
from apps.titanic.app.ports.input.crew_smith_captain_use_case import SmithCaptainUseCase
from apps.titanic.dependencies.crew_smith_captain_provider import get_smith_captain_use_case
from apps.titanic.app.ports.input.passenger_jack_trainer_use_case import JackTrainerUseCase
from apps.titanic.app.ports.input.passenger_rose_model_use_case import RoseModelUseCase
from apps.titanic.dependencies.passenger_jack_trainer_provider import get_jack_trainer_use_case
from apps.titanic.dependencies.passenger_rose_model_provider import get_rose_model_use_case


'''
스미스 선장 (Captain Edward John Smith)
타이타닉의 총책임자. 침몰하는 배와 운명을 함께한 명장.
전체 승객 현황(생존/사망 통계)을 관장하는 마스터 역할.

추천 파일명: smith_captain_router.py (또는 smith_wheel_router.py)
'''
logger = logging.getLogger("apps")
smith_captain_router = APIRouter(prefix="/smith", tags=["smith"])

@smith_captain_router.post("/chat", response_model=SmithCaptainChatResponseSchema)
async def chat(
    schema: Annotated[SmithCaptainChatRequestSchema, Body()],
    smith: SmithCaptainUseCase = Depends(get_smith_captain_use_case)
) -> SmithCaptainChatResponseSchema:
    print(f"[스미스 선장] 채팅 입력: {schema.message}", flush=True)
    return await smith.chat(schema)


@smith_captain_router.get("/myself", response_model=SmithCaptainResponseSchema)
async def introduce_myself(
    smith: SmithCaptainUseCase = Depends(get_smith_captain_use_case),
) -> SmithCaptainResponseSchema:
    result = await smith.introduce_myself(
        ChatSchema(
            id=5,
            name="Edward Smith",
        )
    )
    return SmithCaptainResponseSchema(id=result.id, name=result.name)