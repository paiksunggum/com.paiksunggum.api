import logging

from fastapi import APIRouter, Depends, HTTPException

from apps.agora.app.schemas import SignupRequest, SignupResponse
from apps.friday13th.domain.value_objects.role import UserRole

from .....app.ports.input.signup_use_case import SignupUseCase
from .. import get_signup_use_case
from ..schemas import UserRegisterRequest, UserResponse

logger = logging.getLogger("apps")

signup_router = APIRouter(tags=["friday13th-signup"])


def _to_user_response(data: dict) -> UserResponse:
    return UserResponse(
        id=data["id"],
        user_id=data["user_id"],
        email=data["email"],
        name=data["name"],
        birthdate=data["birthdate"],
        gender=data["gender"],
        role=data["role"],
    )


@signup_router.post("/signup", response_model=SignupResponse)
async def signup(
    req: SignupRequest,
    use_case: SignupUseCase = Depends(get_signup_use_case),
) -> SignupResponse:
    logger.info("[라우터→유스케이스] 회원가입 요청 | userId=%s", req.userId)
    try:
        await use_case.signup(
            user_id=req.userId,
            password=req.password,
            email=req.email or "",
            name=req.name,
            birthdate=req.birthdate,
            gender=req.gender,
            role=UserRole.USER.value,
        )
    except ValueError as e:
        raise HTTPException(status_code=409, detail=str(e)) from e
    except RuntimeError as e:
        raise HTTPException(status_code=503, detail=str(e)) from e
    return SignupResponse(message="회원가입이 완료되었습니다.")


@signup_router.post("/secom/users/register", response_model=UserResponse)
async def secom_signup(
    req: UserRegisterRequest,
    use_case: SignupUseCase = Depends(get_signup_use_case),
) -> UserResponse:
    logger.info("[라우터→유스케이스] secom 회원가입 | user_id=%s", req.user_id)
    try:
        data = await use_case.signup(
            user_id=req.user_id,
            password=req.password,
            email=req.email,
            name=req.name,
            birthdate=req.birthdate,
            gender=req.gender,
            role=req.role.value if hasattr(req.role, "value") else str(req.role),
        )
    except ValueError as e:
        raise HTTPException(status_code=409, detail=str(e)) from e
    except RuntimeError as e:
        raise HTTPException(status_code=503, detail=str(e)) from e
    return _to_user_response(data)
