from pydantic import BaseModel


class UserLoginSchema(BaseModel):
    """로그인 시 레이어 간 전달 (폼 이메일은 user_id에 담음)."""

    user_id: str
    password: str


class UserLoginResponse(BaseModel):
    ok: bool = True
    message: str = "로그인 요청을 받았습니다."
