from pydantic import BaseModel, Field

class AndrewBlueprintSchema(BaseModel):
    id: int = Field(6, description="Andrew Blueprint ID")
    name: str = Field("Andrew Blueprint", description="Andrew Blueprint's name")
    memo: str = Field(
        "타이타닉의 일등 항해사, 승객 명단 관리 담당",
        description="Andrew Blueprint memo",
    )

    model_config = {
        "json_schema_extra": {
            "example": {
                "id": 6,
                "name": "Andrew Blueprint",
                "memo": "타이타닉의 일등 항해사, 승객 명단 관리 담당",
            }
        }
    }


class AndrewBlueprintResponseSchema(BaseModel):
    id: int = Field(6, description="Andrew Blueprint ID")
    name: str = Field("Andrew Blueprint", description="Andrew Blueprint's name")
    memo: str = Field(
        "타이타닉의 일등 항해사, 승객 명단 관리 담당",
        description="Andrew Blueprint memo",
    )

    model_config = {
        "json_schema_extra": {
            "example": {
                "id": 6,
                "name": "Andrew Blueprint",
                "memo": "타이타닉의 일등 항해사, 승객 명단 관리 담당",
            }
        }
    }