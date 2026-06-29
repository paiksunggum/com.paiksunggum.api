from __future__ import annotations

import json
import logging
import re

from apps.automode.app.dtos.email_request_dto import EmailSendCommand, EmailSendResult
from apps.automode.app.ports.input.i_email_send_use_case import IEmailSendUseCase
from apps.automode.app.ports.output.i_email_gateway import IEmailGateway
from apps.automode.domain.entities.email_message import EmailMessage
from core.lol.faker_orchestrator import FakerOrchestrator

logger = logging.getLogger("apps")

_PROMPT = """
다음 요청에 맞는 이메일을 작성하세요. 반드시 아래 JSON 형식으로만 응답하세요.
요청: {prompt}

응답 형식:
{{"subject": "이메일 제목", "body": "이메일 본문"}}
"""


class EmailSendInteractor(IEmailSendUseCase):
    def __init__(self, orchestrator: FakerOrchestrator, gateway: IEmailGateway) -> None:
        self._orchestrator = orchestrator
        self._gateway = gateway

    def _extract_json(self, raw: str) -> dict:
        raw = raw.strip()
        logger.debug("EmailSendInteractor raw response: %s", raw)
        # 코드블록 안 JSON 추출 (```json ... ```)
        m = re.search(r"```(?:json)?\s*(\{.*?\})\s*```", raw, re.DOTALL)
        if m:
            return json.loads(m.group(1))
        # 중괄호 블록 직접 추출
        m = re.search(r"\{.*\}", raw, re.DOTALL)
        if m:
            return json.loads(m.group(0))
        raise ValueError(f"JSON을 찾을 수 없습니다. raw={raw!r}")

    async def send(self, command: EmailSendCommand) -> EmailSendResult:
        raw = await self._orchestrator.ask(_PROMPT.format(prompt=command.prompt))
        parsed = self._extract_json(raw)
        message = EmailMessage(
            to=command.to,
            subject=parsed["subject"],
            body=parsed["body"],
        )
        await self._gateway.send(message)
        logger.info(
            "EmailSendInteractor: sent to=%s subject=%s", message.to, message.subject
        )
        return EmailSendResult(to=message.to, subject=message.subject, success=True)
