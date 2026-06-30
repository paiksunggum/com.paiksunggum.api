from __future__ import annotations

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from apps.automode.adapter.outbound.repositories.email_introduce_repository import (
    EmailIntroduceRepository,
)
from apps.automode.app.ports.input.i_email_introduce_use_case import (
    IEmailIntroduceUseCase,
)
from apps.automode.app.ports.output.i_email_introduce_port import IEmailIntroducePort
from apps.automode.app.use_cases.email_introduce_interactor import (
    EmailIntroduceInteractor,
)
from core.matrix.oracle_database import get_db


def get_email_introduce_repository(
    db: AsyncSession = Depends(get_db),
) -> IEmailIntroducePort:
    return EmailIntroduceRepository(session=db)


def get_email_introduce_use_case(
    repository: IEmailIntroducePort = Depends(get_email_introduce_repository),
) -> IEmailIntroduceUseCase:
    return EmailIntroduceInteractor(repository=repository)
