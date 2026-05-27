from ...domain.entities.titanic import TitanicPassenger
from ..ports.input.titanic_command_port import TitanicCommandPort
from ..ports.output.titanic_passenger_repository_port import TitanicPassengerRepositoryPort


class TitanicCommandImpl:
    def __init__(self, repository: TitanicPassengerRepositoryPort) -> None:
        self._repository = repository

    def create_passenger(self, passenger: TitanicPassenger) -> TitanicPassenger:
        return self._repository.save(passenger)
