from __future__ import annotations

import logging

from fastapi import APIRouter, Depends

from apps.automode.adapter.inbound.api.schemas.email_schema import (
    EmailSendResponseSchema,
    EmailSendSchema,
)
from apps.automode.app.dtos.email_request_dto import EmailSendCommand
from apps.automode.app.ports.input.i_email_send_use_case import IEmailSendUseCase
from apps.automode.dependencies.email_send_provider import get_email_send_use_case

logger = logging.getLogger("apps")
email_router = APIRouter(prefix="/email", tags=["automode"])


@email_router.post("/send", response_model=EmailSendResponseSchema)
async def send_email(
    schema: EmailSendSchema,
    use_case: IEmailSendUseCase = Depends(get_email_send_use_case),
) -> EmailSendResponseSchema:
    result = await use_case.send(EmailSendCommand(to=schema.to, prompt=schema.prompt))
    return EmailSendResponseSchema(
        to=result.to, subject=result.subject, success=result.success
    )
