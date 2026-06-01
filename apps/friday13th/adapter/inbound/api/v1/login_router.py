import logging

from fastapi import APIRouter, Depends, HTTPException

from .....app.ports.input.login_use_case import LoginUseCase
from .. import get_login_use_case
from ..schemas import UserLoginResponse, UserLoginSchema

logger = logging.getLogger("apps")

login_router = APIRouter(tags=["friday13th-login"])


@login_router.post("/login", response_model=UserLoginResponse)
async def login(
    req: UserLoginSchema,
    use_case: LoginUseCase = Depends(get_login_use_case),
) -> UserLoginResponse:
    logger.info("[라우터→유스케이스] 로그인 요청 | user_id=%s", req.user_id)
    try:
        await use_case.login(req.user_id, req.password)
    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e)) from e
    except RuntimeError as e:
        raise HTTPException(status_code=503, detail=str(e)) from e
    return UserLoginResponse(message="로그인에 성공했습니다.")
