from __future__ import annotations

import json
import logging
import re

from apps.automode.app.dtos.email_request_dto import EmailSendCommand, EmailSendResult
from apps.automode.app.ports.input.i_email_send_use_case import IEmailSendUseCase
from apps.automode.app.ports.output.i_email_gateway import IEmailGateway
from apps.automode.app.ports.output.i_slm_client import ISLMClient
from apps.automode.domain.entities.email_message import EmailMessage
from apps.star_craft.domain.ontology.email import EmailOntology
from apps.star_craft.domain.ontology.email.email_type import EmailType

logger = logging.getLogger("apps")

_PROMPT = """
다음 요청에 맞는 이메일을 작성하세요. 반드시 아래 JSON 형식으로만 응답하세요.

작성 규칙: {template_rule}
요청: {prompt}

주의사항:
- **굵게**, *기울임* 같은 마크다운 기호를 절대 사용하지 마세요.
- 문단 구분은 빈 줄(\\n\\n)로 하세요.
- 순수 텍스트로만 작성하세요.

응답 형식:
{{"subject": "이메일 제목", "body": "이메일 본문"}}
"""


class EmailSendInteractor(IEmailSendUseCase):
    def __init__(self, slm: ISLMClient, gateway: IEmailGateway) -> None:
        self._slm = slm
        self._gateway = gateway

    def _extract_json(self, raw: str) -> dict:
        raw = raw.strip()
        logger.debug("EmailSendInteractor raw response: %s", raw)

        candidates: list[str] = []
        m = re.search(r"```(?:json)?\s*(\{.*?\})\s*```", raw, re.DOTALL)
        if m:
            candidates.append(m.group(1))
        m2 = re.search(r"\{.*\}", raw, re.DOTALL)
        if m2:
            candidates.append(m2.group(0))

        for candidate in candidates:
            try:
                return json.loads(candidate, strict=False)
            except json.JSONDecodeError:
                pass

        # JSON 파싱 실패 시 정규식으로 subject/body 직접 추출
        subject_m = re.search(r'"subject"\s*:\s*"(.*?)"(?=\s*,|\s*\})', raw, re.DOTALL)
        body_m = re.search(r'"body"\s*:\s*"(.*?)"(?=\s*\})', raw, re.DOTALL)
        if subject_m and body_m:
            logger.warning("JSON 파싱 실패, 정규식 폴백 사용")
            return {
                "subject": subject_m.group(1),
                "body": body_m.group(1).replace("\\n", "\n"),
            }

        raise ValueError(f"JSON을 찾을 수 없습니다. raw={raw!r}")

    async def send(self, command: EmailSendCommand) -> EmailSendResult:
        template_rule = EmailOntology.get_template_rule(EmailType.FORMAL)
        logger.info("[automode] 온톨로지 규칙 적용: %s", template_rule)

        logger.info("[automode] Exaone SLM 호출 중...")
        raw = await self._slm.ask(
            _PROMPT.format(template_rule=template_rule, prompt=command.prompt)
        )
        logger.info("[automode] Exaone SLM 응답 수신 완료")

        parsed = self._extract_json(raw)
        message = EmailMessage(
            to=command.to,
            subject=parsed["subject"],
            body=parsed["body"],
        )
        await self._gateway.send(message)
        logger.info(
            "[automode] N8n 발송 완료 to=%s subject=%s", message.to, message.subject
        )
        return EmailSendResult(to=message.to, subject=message.subject, success=True)
