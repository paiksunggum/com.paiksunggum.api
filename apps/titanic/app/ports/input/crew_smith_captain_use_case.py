from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any

from apps.titanic.adapter.inbound.api.schemas.crew_smith_captain_schema import (
    SmithCaptainChatRequestSchema,
    ChatSchema,
)
from apps.titanic.app.dtos.crew_smith_captain_dto import SmithCaptainResponse, SmithCaptainChatResult
from apps.titanic.app.ports.input.passenger_jack_trainer_use_case import JackTrainerUseCase
from apps.titanic.app.ports.input.passenger_rose_model_use_case import RoseModelUseCase

class SmithCaptainUseCase(ABC):

    @abstractmethod
    async def introduce_myself(self, schema: ChatSchema) -> SmithCaptainResponse:
        '''스미스 선장의 자기소개 메소드'''
        pass

    @abstractmethod
    async def chat(self, schema: ChatSchema) -> SmithCaptainChatResult:
        '''스미스 선장과의 채팅'''
        pass