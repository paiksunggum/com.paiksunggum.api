from pydantic import BaseModel, Field


class CaledonValidation:
    def __init__(self):
        pass


class PassengerCreateRequest(BaseModel):
    survived: int = Field(ge=0, le=1, description="생존 여부 (0 = 사망, 1 = 생존)")
    pclass: int = Field(ge=1, le=3, description="티켓 클래스 (1 = 1등석, 2 = 2등석, 3 = 3등석)")
    sex: str = Field(max_length=10, description="성별")
    age: float | None = Field(default=None, description="나이")
    sibsp: int = Field(ge=0, description="함께 탑승한 자녀 / 배우자의 수")
    parch: int = Field(ge=0, description="함께 탑승한 부모님 / 아이들의 수")
    ticket: str = Field(max_length=50, description="티켓 번호")
    fare: float = Field(ge=0, description="탑승 요금")
    cabin: str | None = Field(default=None, max_length=50, description="수하물 번호")
    boat: str | None = Field(default=None, max_length=50, description="탈출한 보트 번호")
    embarked: str | None = Field(default=None, max_length=10, description="선착장 (C, Q, S)")


class PassengerResponse(BaseModel):
    id: int
    survived: int
    pclass: int
    sex: str
    age: float | None
    sibsp: int
    parch: int
    ticket: str
    fare: float
    cabin: str | None
    boat: str | None
    embarked: str | None

    model_config = {"from_attributes": True}
