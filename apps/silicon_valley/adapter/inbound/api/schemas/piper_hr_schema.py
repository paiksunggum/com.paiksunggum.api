from pydantic import BaseModel, Field


class PiperHrResponseSchema(BaseModel):
    id: int
    name: str


class PiperHrSchema(BaseModel):

    id: int = Field(0, description="HR Manager ID")
    name: str = Field("HR 매니저", description="HR Manager name")
    # Pied Piper HR 담당자. 팀원 채용 및 조직 문화 관리

    model_config = {
        "json_schema_extra": {
            "example": {
                "id": 4,
                "name": "HR Manager",
            }
        }
    }
