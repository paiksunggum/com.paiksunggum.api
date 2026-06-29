"""Faker Orchestrator — EXAONE 3.5 7.8B (Ollama) 기반 로컬 오케스트레이터."""

import os

from ollama import AsyncClient, Message

MODEL = "exaone3.5:7.8b"
_DEFAULT_HOST = "http://localhost:11434"


class FakerOrchestrator:
    """EXAONE 3.5 7.8B를 로컬 Ollama로 실행하는 비동기 오케스트레이터."""

    def __init__(
        self,
        model: str = MODEL,
        host: str | None = None,
    ) -> None:
        self.model = model
        self._client = AsyncClient(host=host or os.getenv("OLLAMA_HOST", _DEFAULT_HOST))
        self.model = model
        self._client = AsyncClient(host=host)

    async def chat(self, messages: list[Message]) -> str:
        """대화 이력을 받아 모델 응답 텍스트를 반환한다."""
        response = await self._client.chat(model=self.model, messages=messages)
        return response.message.content

    async def ask(self, prompt: str) -> str:
        """단발 질문 편의 메서드."""
        return await self.chat([{"role": "user", "content": prompt}])
