from core.matrix.theone_base import TheOneBase


class AArchitectORM(TheOneBase):
    """
    [기획 홀딩 구여]
    - 실제 DB 테이블을 생성하지 않고 설계만 유지합니다.
    """
    # 이 한줄이 들어가면 pass와 동일하게 

    __abstract__ = True