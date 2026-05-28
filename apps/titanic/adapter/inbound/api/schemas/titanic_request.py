from pydantic import BaseModel, ConfigDict, Field


class TitanicPassengerRowRequest(BaseModel):
    """
    Titanic 한 row(1개 승객)의 입력 스키마.

    이미지의 컬럼을 기준으로 구성하며,
    `Sex` 컬럼은 스키마 필드명을 `gender`로 변형한다.
    """

    model_config = ConfigDict(populate_by_name=True)

    passenger_id: str = Field(description="PassengerId", alias="PassengerId")
    survived: str = Field(description="Survived", alias="Survived")
    pclass: str = Field(description="Pclass", alias="Pclass")
    name: str = Field(description="Name", alias="Name")
    gender: str = Field(description="Gender (Sex -> gender)", alias="Sex")
    age: str = Field(description="Age", alias="Age")
    sibsp: str = Field(description="SibSp", alias="SibSp")
    parch: str = Field(description="Parch", alias="Parch")
    ticket: str = Field(description="Ticket", alias="Ticket")
    fare: str = Field(description="Fare", alias="Fare")
    cabin: str = Field(description="Cabin", alias="Cabin")
    embarked: str = Field(description="Embarked", alias="Embarked")

