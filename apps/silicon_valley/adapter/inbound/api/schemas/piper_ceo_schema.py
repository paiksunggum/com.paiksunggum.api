from pydantic import BaseModel, Field


class PiperCeoResponseSchema(BaseModel):
    id: int
    name: str


class PiperCeoSchema(BaseModel):

    id: int = Field(0, description="CEO ID")
    name: str = Field("리처드 헨드릭스", description="CEO name")
    # Pied Piper CEO. 중간값 압축 알고리즘을 개발한 천재 엔지니어

    model_config = {
        "json_schema_extra": {
            "example": {
                "id": 1,
                "name": "Richard Hendricks",
            }
        }
    }
