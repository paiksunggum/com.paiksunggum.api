from __future__ import annotations

import logging

from fastapi import APIRouter, Depends

from apps.automode.adapter.inbound.api.schemas.email_schema import (
    EmailClassifyResponseSchema,
    EmailClassifySchema,
    EmailIntroduceResponseSchema,
    EmailSendResponseSchema,
    EmailSendSchema,
)
from apps.automode.app.dtos.email_request_dto import (
    EmailClassifyCommand,
    EmailIntroduceQuery,
    EmailSendCommand,
)
from apps.automode.app.ports.input.email_classify_use_case import EmailClassifyUseCase
from apps.automode.app.ports.input.email_introduce_use_case import EmailIntroduceUseCase
from apps.automode.app.ports.input.email_send_use_case import EmailSendUseCase
from apps.automode.dependencies.email_classify_provider import (
    get_email_classify_use_case,
)
from apps.automode.dependencies.email_introduce_provider import (
    get_email_introduce_use_case,
)
from apps.automode.dependencies.email_send_provider import get_email_send_use_case

logger = logging.getLogger("apps")
email_router = APIRouter(prefix="/email", tags=["automode"])


@email_router.post("/send", response_model=EmailSendResponseSchema)
async def send_email(
    schema: EmailSendSchema,
    use_case: EmailSendUseCase = Depends(get_email_send_use_case),
) -> EmailSendResponseSchema:
    logger.info("[automode] 이메일 발송 요청 수신 to=%s", schema.to)
    result = await use_case.send(
        EmailSendCommand(
            to=schema.to,
            prompt=schema.prompt,
            to_name=schema.to_name or "",
        )
    )
    logger.info("[automode] 발송 완료 to=%s subject=%s", result.to, result.subject)
    return EmailSendResponseSchema(
        to=result.to, subject=result.subject, success=result.success
    )


@email_router.post("/classify", response_model=EmailClassifyResponseSchema)
async def classify_email(
    schema: EmailClassifySchema,
    use_case: EmailClassifyUseCase = Depends(get_email_classify_use_case),
) -> EmailClassifyResponseSchema:
    logger.info("[automode] 스팸 분류 요청 subject=%s", schema.subject)
    result = await use_case.classify(
        EmailClassifyCommand(subject=schema.subject, body=schema.body)
    )
    logger.info(
        "[automode] 분류 완료 category=%s spam=%s", result.category, result.is_spam
    )
    return EmailClassifyResponseSchema(
        category=result.category.value,
        matched_keywords=result.matched_keywords,
        is_spam=result.is_spam,
    )


@email_router.get("/myself", response_model=EmailIntroduceResponseSchema)
async def introduce_myself(
    use_case: EmailIntroduceUseCase = Depends(get_email_introduce_use_case),
) -> EmailIntroduceResponseSchema:
    logger.info("[automode] 이메일 서비스 자기소개 요청")
    result = await use_case.introduce_myself(EmailIntroduceQuery(id=1, name="이메일"))
    return EmailIntroduceResponseSchema(id=result.id, name=result.name)
