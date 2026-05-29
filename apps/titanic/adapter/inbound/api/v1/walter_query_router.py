import logging

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from apps.database import get_db
from .....app.ports.input.walter_query_use_case import WalterQueryUseCase
from .....app.ports.input.titanic_query_port import TitanicQueryPort
from .....app.use_cases.titanic_query_impl import TitanicQueryImpl
from .....app.use_cases.walter_passenger_query import WalterPassengerQuery
from ....outbound.pg.rose_model_adapter import RoseModelAdapter
from ....outbound.pg.walter_pg_repository import WalterPgRepository
from ....outbound.pg.walter_reader_adapter import WalterReaderAdapter

walter_router = APIRouter(prefix="/titanic")
logger = logging.getLogger("apps")

_query_use_case = TitanicQueryImpl(
    data_reader=WalterReaderAdapter(),
    model=RoseModelAdapter(),
)


def get_titanic_query_port() -> TitanicQueryPort:
    return _query_use_case


def get_walter_query_use_case() -> WalterQueryUseCase:
    return WalterPassengerQuery(WalterPgRepository())


@walter_router.get("/data", tags=["titanic-query"])
def read_titanic_data(query: TitanicQueryPort = Depends(get_titanic_query_port)):
    try:
        df = query.get_data()
        return df.to_dict(orient="records")
    except RuntimeError as e:
        raise HTTPException(status_code=501, detail=str(e)) from e


@walter_router.get("/count", tags=["titanic-query"])
def read_titanic_count(query: TitanicQueryPort = Depends(get_titanic_query_port)):
    try:
        count = query.get_count()
        return {"count": count}
    except RuntimeError as e:
        raise HTTPException(status_code=501, detail=str(e)) from e


@walter_router.get("/tree", tags=["titanic-query"])
def read_titanic_tree(query: TitanicQueryPort = Depends(get_titanic_query_port)):
    tree = query.has_decision_tree_model()
    return {"tree": tree}


@walter_router.get("/model", tags=["titanic-query"])
def read_titanic_model(query: TitanicQueryPort = Depends(get_titanic_query_port)):
    return query.get_model_name_and_accuracy()


@walter_router.get("/walter/passengers", tags=["walter"])
async def read_walter_passengers(
    page: int = 1,
    page_size: int = 50,
    db: AsyncSession = Depends(get_db),
    walter_query: WalterQueryUseCase = Depends(get_walter_query_use_case),
):
    logger.info(
        "[라우터→유스케이스] 승객 조회 요청 수신 | 경로=/titanic/walter/passengers, page=%d, page_size=%d",
        page,
        page_size,
    )
    return await walter_query.get_passengers(
        page=page,
        page_size=page_size,
        db=db,
    )
