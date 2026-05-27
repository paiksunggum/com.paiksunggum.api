from typing import Protocol

from ....domain.entities.titanic import TitanicPassenger


class TitanicCommandPort(Protocol):
    def create_passenger(self, passenger: TitanicPassenger) -> TitanicPassenger:
        ...
