from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from core.matrix.oracle_database import get_db
from apps.admin.adapter.outbound.pg.users_ad_pg_repository import UsersAdPgRepository
from apps.admin.app.ports.input.users_ad_use_case import UsersAdUseCase
from apps.admin.app.ports.output.users_ad_repository import UsersAdRepository
from apps.admin.app.use_cases.users_ad_interactor import UsersAdInteractor


def get_users_ad_use_case(
        db: AsyncSession = Depends(get_db),
) -> UsersAdUseCase:
    repository: UsersAdRepository = UsersAdPgRepository(session=db)
    return UsersAdInteractor(repository=repository)
