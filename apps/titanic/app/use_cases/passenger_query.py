from sqlmodel import Field, SQLModel


class Passenger(SQLModel):
    """CSV/ML용 레코드. DB 테이블은 사용하지 않습니다."""

    survived: int  # 0 = 사망, 1 = 생존
    pclass: int  # 1 = 1등석, 2 = 2등석, 3 = 3등석
    sex: str = Field(max_length=10)
    age: float | None = Field(default=None)
    sibsp: int = Field(default=0)  # 함께 탑승한 자녀 / 배우자 의 수
    parch: int = Field(default=0)  # 함께 탑승한 부모님 / 아이들 의 수
    ticket: str = Field(max_length=50)
    fare: float = Field(default=0.0)
    cabin: str | None = Field(default=None, max_length=50)
    boat: str | None = Field(default=None, max_length=50)
    embarked: str | None = Field(default=None, max_length=10)
