from pydantic import BaseModel, ConfigDict, Field


class JamesCommandSchema(BaseModel):
    """
    Titanic CSV 한 row(승객 1명) 입력 스키마.

    컬럼: PassengerId, Survived, Pclass, Name, Sex→gender, Age,
    SibSp, Parch, Ticket, Fare, Cabin, Embarked
    """

    model_config = ConfigDict(populate_by_name=True)

    passenger_id: str = Field(alias="PassengerId")
    survived: str = Field(alias="Survived")
    pclass: str = Field(alias="Pclass")
    name: str = Field(alias="Name")
    gender: str = Field(alias="Sex")
    age: str = Field(alias="Age")
    sib_sp: str = Field(alias="SibSp")
    parch: str = Field(alias="Parch")
    ticket: str = Field(alias="Ticket")
    fare: str = Field(alias="Fare")
    cabin: str = Field(default="", alias="Cabin")
    embarked: str = Field(alias="Embarked")


class JamesCommandFileUploadResponse(BaseModel):
    ok: bool = Field(True, description="Upload succeeded")
    inserted: int = Field(891, description="Inserted row count")
    fileName: str = Field("train.csv", description="Uploaded file name")
    columns: list[str] = Field(
        default_factory=lambda: [
            "PassengerId",
            "Survived",
            "Pclass",
            "Name",
            "Sex",
            "Age",
            "SibSp",
            "Parch",
            "Ticket",
            "Fare",
            "Cabin",
            "Embarked",
        ],
        description="Normalized CSV column names",
    )
    dataRowCount: int = Field(891, description="Parsed data row count")

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "ok": True,
                "inserted": 891,
                "fileName": "train.csv",
                "columns": [
                    "PassengerId",
                    "Survived",
                    "Pclass",
                    "Name",
                    "Sex",
                    "Age",
                    "SibSp",
                    "Parch",
                    "Ticket",
                    "Fare",
                    "Cabin",
                    "Embarked",
                ],
                "dataRowCount": 891,
            }
        }
    )
