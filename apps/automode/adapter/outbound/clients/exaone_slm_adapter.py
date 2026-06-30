from __future__ import annotations

import logging
import os

from ollama import AsyncClient

from apps.automode.app.ports.output.i_slm_client import ISLMClient

logger = logging.getLogger("apps")

_MODEL = "exaone3.5:2.4b"
_DEFAULT_HOST = "http://localhost:11434"


class ExaoneSLMAdapter(ISLMClient):
    def __init__(self, model: str = _MODEL, host: str | None = None) -> None:
        self._model = model
        self._client = AsyncClient(host=host or os.getenv("OLLAMA_HOST", _DEFAULT_HOST))

    async def ask(self, prompt: str) -> str:
        logger.info("[ExaoneSLM] 모델=%s 프롬프트 전송", self._model)
        response = await self._client.chat(
            model=self._model,
            messages=[{"role": "user", "content": prompt}],
        )
        logger.info("[ExaoneSLM] 생성 완료 len=%d", len(response.message.content))
        return response.message.content
