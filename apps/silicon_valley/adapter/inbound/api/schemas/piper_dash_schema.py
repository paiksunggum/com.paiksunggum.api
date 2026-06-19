from pydantic import BaseModel, Field


class PiperDashResponseSchema(BaseModel):
    id: int
    name: str


class PiperDashSchema(BaseModel):

    id: int = Field(0, description="Dashboard Manager ID")
    name: str = Field("모니카 홀", description="Dashboard Manager name")
    # Raviga Capital 투자 담당자. Pied Piper의 주요 지지자

    model_config = {
        "json_schema_extra": {
            "example": {
                "id": 3,
                "name": "Monica Hall",
            }
        }
    }
