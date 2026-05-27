from dataclasses import asdict

from fastapi import APIRouter, Depends, HTTPException

from .....app.ports.input.titanic_command_port import TitanicCommandPort
from .....app.use_cases.titanic_command_impl import TitanicCommandImpl
from ....outbound.impl.titanic_passenger_repository_impl import (
    InMemoryTitanicPassengerRepository,
)
from .....domain.entities.titanic import TitanicPassenger
from ...schemas.titanic_request import TitanicPassengerRowRequest
from ...schemas.titanic_response import TitanicPassengerRowResponse

router = APIRouter(prefix="/titanic", tags=["titanic-command"])

_repository = InMemoryTitanicPassengerRepository()
_command_use_case = TitanicCommandImpl(_repository)


def get_titanic_command_port() -> TitanicCommandPort:
    return _command_use_case


def _to_entity(req: TitanicPassengerRowRequest) -> TitanicPassenger:
    return TitanicPassenger(**req.model_dump(by_alias=False))


def _to_response(passenger: TitanicPassenger) -> TitanicPassengerRowResponse:
    return TitanicPassengerRowResponse.model_validate(asdict(passenger))


@router.post("/passengers", response_model=TitanicPassengerRowResponse)
def create_passenger(
    req: TitanicPassengerRowRequest,
    command: TitanicCommandPort = Depends(get_titanic_command_port),
):
    try:
        saved = command.create_passenger(_to_entity(req))
        return _to_response(saved)
    except ValueError as e:
        raise HTTPException(status_code=409, detail=str(e)) from e


@router.post("/passengers/bulk", response_model=list[TitanicPassengerRowResponse])
def create_passengers_bulk(
    req: list[TitanicPassengerRowRequest],
    command: TitanicCommandPort = Depends(get_titanic_command_port),
):
    saved: list[TitanicPassengerRowResponse] = []
    for row in req:
        try:
            passenger = command.create_passenger(_to_entity(row))
            saved.append(_to_response(passenger))
        except ValueError as e:
            raise HTTPException(status_code=409, detail=str(e)) from e
    return saved
