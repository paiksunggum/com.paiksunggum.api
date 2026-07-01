from __future__ import annotations

from apps.automode.app.dtos.email_request_dto import (
    EmailIntroduceQuery,
    EmailIntroduceResult,
)
from apps.automode.app.ports.input.email_introduce_use_case import EmailIntroduceUseCase
from apps.automode.app.ports.output.email_introduce_port import EmailIntroducePort


class EmailIntroduceInteractor(EmailIntroduceUseCase):
    def __init__(self, repository: EmailIntroducePort) -> None:
        self._repository = repository

    async def introduce_myself(
        self, query: EmailIntroduceQuery
    ) -> EmailIntroduceResult:
        return await self._repository.introduce_myself(query)
