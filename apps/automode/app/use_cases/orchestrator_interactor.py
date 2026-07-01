"""오케스트레이터 인터랙터.

EXAONE 7.8B가 사용자 명령을 분석해 어떤 툴을 쓸지 결정한다.
실제 실행은 FakerOrchestrator가 위임받아 처리한다.
"""

from __future__ import annotations

import json
import logging
import re
from typing import Any

from apps.automode.app.ports.input.orchestrator_use_case import OrchestratorUseCase
from apps.automode.app.ports.output.slm_port import SLMPort
from core.lol.faker_orchestrator import FakerOrchestrator

logger = logging.getLogger("apps")

_TOOL_SPEC = [
    {
        "name": "email_send",
        "description": "이메일 발송. 수신자와 내용 요청을 받아 AI가 작성 후 발송한다.",
        "args": {
            "to": "수신자 이메일 주소 (실제 이메일 형식)",
            "to_name": "수신자 이름",
            "prompt": "이메일 내용 요청 (예: 안부 인사 메일 써줘)",
        },
    },
    {
        "name": "telegram_send",
        "description": "개발자 스마트폰 텔레그램으로 메시지 전송",
        "args": {"text": "전송할 메시지 내용"},
    },
]

_PROMPT_TEMPLATE = """\
당신은 AI 오케스트레이터입니다. 사용자 명령을 분석하고 아래 도구 중 하나를 선택하세요.

사용 가능한 도구:
{tools}

주소록 (이름 → 이메일):
{contacts}

사용자 명령: {message}

반드시 JSON 한 줄로만 응답하세요 (다른 텍스트 절대 금지):
{{"tool": "도구이름", "args": {{...}}}}"""


class OrchestratorInteractor(OrchestratorUseCase):
    def __init__(self, slm: SLMPort, orchestrator: FakerOrchestrator) -> None:
        self._slm = slm
        self._orchestrator = orchestrator

    async def handle(
        self, message: str, contacts: dict[str, str] | None = None
    ) -> dict[str, Any]:
        contacts_str = (
            "\n".join(f"- {name}: {email}" for name, email in (contacts or {}).items())
            or "없음"
        )
        prompt = _PROMPT_TEMPLATE.format(
            tools=json.dumps(_TOOL_SPEC, ensure_ascii=False, indent=2),
            contacts=contacts_str,
            message=message,
        )
        raw = await self._slm.ask(prompt)
        logger.info("[orchestrator] LLM 응답: %s", raw)

        decision = self._parse(raw)
        logger.info(
            "[orchestrator] 결정: tool=%s args=%s", decision["tool"], decision["args"]
        )

        result = await self._orchestrator.dispatch(decision["tool"], decision["args"])
        return {"tool": decision["tool"], "result": result}

    @staticmethod
    def _parse(raw: str) -> dict:
        m = re.search(r"\{.*\}", raw, re.DOTALL)
        if not m:
            raise ValueError(f"LLM이 JSON을 반환하지 않았습니다: {raw!r}")
        return json.loads(m.group())
