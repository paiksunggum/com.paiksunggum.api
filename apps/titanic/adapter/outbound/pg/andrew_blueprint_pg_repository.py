from sqlalchemy.ext.asyncio import AsyncSession

from apps.titanic.app.dtos.andrew_blueprint_dto import AndrewBlueprintQuery
from apps.titanic.app.ports.output.andrew_blueprint_repository import AndrewBlueprintRepository
import logging
logger = logging.getLogger("apps")


class AndrewBlueprintPgRepository(AndrewBlueprintRepository):
    '''PostgreSQL을 이용한 앤드류의 승객 명단 관리 저장소'''

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    def introduce_myself(self, query: AndrewBlueprintQuery):
        '''승객 명단을 가져오는 메소드'''
        # PostgreSQL에서 승객 명단을 가져오는 로직 구현
        logger.info("##################################################")
        logger.info("🎶[앤드류 레포지터리] 앤드류의 자기소개글을 가져오는 데이터베이스 호출")
        logger.info("🐱‍👤ID: %s", query.id)
        logger.info("🐱‍👓이름: %s", query.name)
        logger.info("🐱‍🐉메모: %s", query.memo)
        logger.info("##################################################")

        pass