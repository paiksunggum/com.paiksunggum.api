from abc import ABC, abstractmethod

from apps.titanic.adapter.inbound.api.schemas.crew_andrew_blueprint_schema import AndrewBlueprintSchema
from apps.titanic.app.dtos.crew_andrew_blueprint_dto import AndrewBlueprintResponse


class AndrewBlueprintUseCase(ABC):
    @abstractmethod
    async def introduce_myself(self,
        schema: AndrewBlueprintSchema,
    ) -> AndrewBlueprintResponse:
        pass