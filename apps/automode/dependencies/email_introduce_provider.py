from __future__ import annotations

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from apps.automode.adapter.outbound.repositories.email_introduce_repository import (
    EmailIntroduceRepository,
)
from apps.automode.app.ports.input.email_introduce_use_case import EmailIntroduceUseCase
from apps.automode.app.ports.output.email_introduce_port import EmailIntroducePort
from apps.automode.app.use_cases.email_introduce_interactor import (
    EmailIntroduceInteractor,
)
from core.matrix.oracle_database import get_db


def get_email_introduce_repository(
    db: AsyncSession = Depends(get_db),
) -> EmailIntroducePort:
    return EmailIntroduceRepository(session=db)


def get_email_introduce_use_case(
    repository: EmailIntroducePort = Depends(get_email_introduce_repository),
) -> EmailIntroduceUseCase:
    return EmailIntroduceInteractor(repository=repository)
