from fastapi import APIRouter
from apps.titanic.adapter.inbound.api.schemas.andrew_blueprint_schema import AndrewBlueprintSchema
from apps.titanic.app.ports.input.andrew_blueprint_use_case import AndrewBlueprintUseCase
from apps.titanic.app.use_cases.andrew_blueprint_interactor import AndrewBlueprintInteractor
import logging
logger = logging.getLogger("apps")
andrew_blueprint_router = APIRouter(prefix="/andrew", tags=["andrew"])



@andrew_blueprint_router.get("/myself")
async def introduce_myself():
    schema = AndrewBlueprintSchema()

    logger.info("##################################################")
    logger.info("🎶[앤드류 라우터] 앤드류의 자기소개글을 가져오는 API 호출")
    logger.info(f"🐱‍👤ID: {schema.id}")
    logger.info(f"🐱‍👓이름: {schema.name}")
    logger.info(f"🐱‍🐉메모: {schema.memo}")
    logger.info("##################################################")


    andrew: AndrewBlueprintUseCase = AndrewBlueprintInteractor()
    andrew.introduce_myself(schema)

    pass