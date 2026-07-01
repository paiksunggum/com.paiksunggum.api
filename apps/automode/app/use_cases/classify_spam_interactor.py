from __future__ import annotations

import json
import logging
import re

from apps.automode.app.dtos.email_request_dto import (
    EmailClassifyCommand,
    EmailClassifyResult,
)
from apps.automode.app.ports.input.email_classify_use_case import EmailClassifyUseCase
from apps.automode.app.ports.output.slm_port import SLMPort
from apps.star_craft.domain.ontology.spam.spam_category import SpamCategory

logger = logging.getLogger("apps")

_CATEGORIES = ", ".join(c.value for c in SpamCategory)

_PROMPT = """\
다음 이메일이 스팸인지 판단하세요.

제목: {subject}
본문: {body}

스팸 카테고리:
- phishing: 피싱 (개인정보·계정 탈취 시도)
- promotional: 광고·홍보성 메일
- malware: 악성코드·바이러스 포함
- scam: 사기 (금융·투자 등)
- legitimate: 정상 메일

반드시 JSON 한 줄로만 응답하세요 (다른 텍스트 금지):
{{"is_spam": true/false, "category": "카테고리"}}"""


class ClassifySpamInteractor(EmailClassifyUseCase):
    def __init__(self, slm: SLMPort) -> None:
        self._slm = slm

    async def classify(self, command: EmailClassifyCommand) -> EmailClassifyResult:
        prompt = _PROMPT.format(subject=command.subject, body=command.body)
        raw = await self._slm.ask(prompt)
        logger.info("[spam] LLM 응답: %s", raw)

        parsed = self._parse(raw)
        raw_category = parsed.get("category", SpamCategory.LEGITIMATE.value)
        try:
            category = SpamCategory(raw_category)
        except ValueError:
            logger.warning("[spam] 알 수 없는 카테고리, 정상 처리: %r", raw_category)
            category = SpamCategory.LEGITIMATE
        is_spam = bool(parsed.get("is_spam", False))

        return EmailClassifyResult(
            category=category,
            matched_keywords=[],
            is_spam=is_spam,
        )

    @staticmethod
    def _parse(raw: str) -> dict:
        m = re.search(r"\{.*\}", raw, re.DOTALL)
        if not m:
            logger.warning("[spam] JSON 파싱 실패, 정상 메일로 처리: %r", raw)
            return {"is_spam": False, "category": "legitimate"}
        try:
            return json.loads(m.group())
        except json.JSONDecodeError:
            logger.warning("[spam] JSON 디코드 실패, 정상 메일로 처리")
            return {"is_spam": False, "category": "legitimate"}
