from fastapi import APIRouter, Depends, HTTPException

from .....app.ports.input.titanic_query_port import TitanicQueryPort
from .....app.use_cases.titanic_query_impl import TitanicQueryImpl
from ....outbound.impl.rose_model_adapter import RoseModelAdapter
from ....outbound.impl.walter_reader_adapter import WalterReaderAdapter

router = APIRouter(prefix="/titanic", tags=["titanic-query"])

_query_use_case = TitanicQueryImpl(
    data_reader=WalterReaderAdapter(),
    model=RoseModelAdapter(),
)


def get_titanic_query_port() -> TitanicQueryPort:
    return _query_use_case


@router.get("/data")
def read_titanic_data(query: TitanicQueryPort = Depends(get_titanic_query_port)):
    try:
        df = query.get_data()
        return df.to_dict(orient="records")
    except RuntimeError as e:
        raise HTTPException(status_code=501, detail=str(e)) from e


@router.get("/count")
def read_titanic_count(query: TitanicQueryPort = Depends(get_titanic_query_port)):
    try:
        count = query.get_count()
        return {"count": count}
    except RuntimeError as e:
        raise HTTPException(status_code=501, detail=str(e)) from e


@router.get("/tree")
def read_titanic_tree(query: TitanicQueryPort = Depends(get_titanic_query_port)):
    tree = query.has_decision_tree_model()
    return {"tree": tree}


@router.get("/model")
def read_titanic_model(query: TitanicQueryPort = Depends(get_titanic_query_port)):
    return query.get_model_name_and_accuracy()
