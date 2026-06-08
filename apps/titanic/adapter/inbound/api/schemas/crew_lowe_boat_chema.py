from pydantic import BaseModel, Field

class LoweBoatSchema(BaseModel):
    
    id: int = Field(0, description="Officer ID")
    name: str = Field("해롤드 로우", description="Officer's name")
    
    model_config = {
        "json_schema_extra": {
            "example": {
                "id": 4,
                "name": "Harold Lowe",
            }
        }
    }


class LoweBoatResponseSchema(BaseModel):
    id: int = Field(4, description="Officer ID")
    name: str = Field("Harold Lowe", description="Officer's name")

    model_config = {
        "json_schema_extra": {
            "example": {
                "id": 4,
                "name": "Harold Lowe",
            }
        }
    }