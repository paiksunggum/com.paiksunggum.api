from apps.titanic.adapter.inbound.api.schemas.andrew_blueprint_schema import AndrewBlueprintSchema
from apps.titanic.adapter.outbound.pg.andrew_blueprint_pg_repository import AndrewBlueprintPgRepository
from apps.titanic.app.dtos.andrew_blueprint_dto import AndrewBlueprintQuery
from apps.titanic.app.ports.input.andrew_blueprint_use_case import AndrewBlueprintUseCase
from apps.titanic.app.ports.output.andrew_blueprint_repository import AndrewBlueprintRepository
import logging
logger = logging.getLogger("apps")

class AndrewBlueprintInteractor(AndrewBlueprintUseCase):
    def __init__(self):
        pass

    def introduce_myself(self, schema: AndrewBlueprintSchema):
        '''앤드류의 자기소개 메소드'''
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

        andrew: AndrewBlueprintRepository = AndrewBlueprintPgRepository()
        andrew.introduce_myself(query)

        pass
