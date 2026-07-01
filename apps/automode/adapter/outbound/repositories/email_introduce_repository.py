from __future__ import annotations

from sqlalchemy.ext.asyncio import AsyncSession

from apps.automode.app.dtos.email_request_dto import (
    EmailIntroduceQuery,
    EmailIntroduceResult,
)
from apps.automode.app.ports.output.email_introduce_port import EmailIntroducePort


class EmailIntroduceRepository(EmailIntroducePort):
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def introduce_myself(
        self, query: EmailIntroduceQuery
    ) -> EmailIntroduceResult:
        return EmailIntroduceResult(id=query.id, name="AI 이메일 발송 서비스")
