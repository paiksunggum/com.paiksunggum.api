from abc import ABC, abstractmethod

from apps.titanic.adapter.inbound.api.schemas.andrew_blueprint_schema import AndrewBlueprintSchema
from apps.titanic.app.dtos.andrew_blueprint_dto import AndrewBlueprintResponse


class AndrewBlueprintUseCase(ABC):
    @abstractmethod
    async def introduce_myself(
        schema: AndrewBlueprintSchema,
    ) -> AndrewBlueprintResponse:
        ...
