from abc import ABC, abstractmethod

from apps.titanic.app.dtos.andrew_blueprint_dto import AndrewBlueprintQuery


class AndrewBlueprintRepository(ABC):
    @abstractmethod
    def introduce_myself(
        query: AndrewBlueprintQuery,
    ) -> None:
        ...
