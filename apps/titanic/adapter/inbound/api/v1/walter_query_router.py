import logging

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_db

from ....outbound.pg.walter_pg_repository import WalterPgRepository

walter_router = APIRouter(prefix="/titanic")
logger = logging.getLogger("apps")

_walter_pg = WalterPgRepository()


@walter_router.get("/walter/passengers", tags=["walter"])
async def read_walter_passengers(
    page: int = 1,
    page_size: int = 50,
    db: AsyncSession = Depends(get_db),
):
    logger.info(
        "[라우터→저장소] 승객 조회 | page=%d, page_size=%d",
        page,
        page_size,
    )
    return await _walter_pg.get_passengers(
        page=page,
        page_size=page_size,
        db=db,
    )
