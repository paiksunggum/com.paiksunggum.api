from __future__ import annotations

from apps.automode.app.dtos.email_request_dto import (
    EmailIntroduceQuery,
    EmailIntroduceResult,
)
from apps.automode.app.ports.input.i_email_introduce_use_case import (
    IEmailIntroduceUseCase,
)
from apps.automode.app.ports.output.i_email_introduce_port import IEmailIntroducePort


class EmailIntroduceInteractor(IEmailIntroduceUseCase):
    def __init__(self, repository: IEmailIntroducePort) -> None:
        self._repository = repository

    async def introduce_myself(
        self, query: EmailIntroduceQuery
    ) -> EmailIntroduceResult:
        return await self._repository.introduce_myself(query)
