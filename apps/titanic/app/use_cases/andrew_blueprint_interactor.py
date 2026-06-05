import logging

from apps.titanic.adapter.inbound.api.schemas.andrew_blueprint_schema import AndrewBlueprintSchema
from apps.titanic.app.dtos.andrew_blueprint_dto import AndrewBlueprintQuery, AndrewBlueprintResponse
from apps.titanic.app.ports.input.andrew_blueprint_use_case import AndrewBlueprintUseCase
from apps.titanic.app.ports.output.andrew_blueprint_repository import AndrewBlueprintRepository

logger = logging.getLogger("apps")


class AndrewBlueprintInteractor(AndrewBlueprintUseCase):
    def __init__(self, repository: AndrewBlueprintRepository) -> None:
        self._repository = repository

    async def introduce_myself(
        self,
        schema: AndrewBlueprintSchema,
    ) -> AndrewBlueprintResponse:
        query = AndrewBlueprintQuery(
            id=schema.id,
            name=schema.name,
            memo=schema.memo,
        )

        logger.info("##################################################")
        logger.info("🎶[앤드류 유스케이스] 라우터에서 가져온 앤드류 정보")
        logger.info("🐱‍👤ID: %s", query.id)
        logger.info("🐱‍👓이름: %s", query.name)
        logger.info("🐱‍🐉메모: %s", query.memo)
        logger.info("##################################################")

        self._repository.introduce_myself(query)

        return AndrewBlueprintResponse(
            id=query.id,
            name=query.name,
            memo=query.memo,
        )
