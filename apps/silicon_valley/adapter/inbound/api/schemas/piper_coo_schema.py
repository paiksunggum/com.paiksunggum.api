from pydantic import BaseModel, Field


class PiperCooResponseSchema(BaseModel):
    id: int
    name: str


class PiperCooSchema(BaseModel):

    id: int = Field(0, description="COO ID")
    name: str = Field("재러드 던", description="COO name")
    # Pied Piper COO. 본명 Donald Dunn. 회사 운영 전반을 담당하는 비즈니스 총괄

    model_config = {
        "json_schema_extra": {
            "example": {
                "id": 2,
                "name": "Jared Dunn",
            }
        }
    }
