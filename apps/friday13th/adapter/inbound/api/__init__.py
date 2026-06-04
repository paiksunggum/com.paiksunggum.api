"""인바운드 API 조립 — 라우터는 여기서 주입된 use case만 사용한다."""

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.matrix.oracle_database import get_db

from apps.friday13th.app.ports.input.login_use_case import LoginUseCase
from apps.friday13th.app.ports.input.signup_use_case import SignupUseCase


def get_login_use_case(db: AsyncSession = Depends(get_db)) -> LoginUseCase:
    from apps.friday13th.adapter.outbound.pg.login_pg_repository import LoginPgRepository
    from apps.friday13th.app.use_cases.login_interactor import LoginInteractor

    return LoginInteractor(LoginPgRepository(db))


def get_signup_use_case(db: AsyncSession = Depends(get_db)) -> SignupUseCase:
    from apps.friday13th.adapter.outbound.pg.signup_pg_repository import (
        SignupPgRepository,
    )
    from apps.friday13th.app.use_cases.signup_interactor import SignupInteractor

    return SignupInteractor(SignupPgRepository(db))
