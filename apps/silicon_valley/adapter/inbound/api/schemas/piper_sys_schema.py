from pydantic import BaseModel, Field


class PiperSysResponseSchema(BaseModel):
    id: int
    name: str


class PiperSysSchema(BaseModel):

    id: int = Field(0, description="Systems Architect ID")
    name: str = Field("버트람 길포일", description="Systems Architect name")
    # Pied Piper 시스템 아키텍트. 인프라 설계 및 보안 담당

    model_config = {
        "json_schema_extra": {
            "example": {
                "id": 5,
                "name": "Bertram Gilfoyle",
            }
        }
    }
