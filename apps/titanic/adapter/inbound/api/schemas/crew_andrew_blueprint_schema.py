from pydantic import BaseModel, Field


class AndrewBlueprintResponseSchema(BaseModel):

    id: int
    name: str


class AndrewBlueprintSchema(BaseModel):

    id: int = Field(6, description="Andrew Blueprint ID")
    name: str = Field("Andrew Blueprint", description="Andrew Blueprint's name")
         # 타이타닉 기관실 인력. 숨겨진 영웅들인 화부와 불을 끄던 스토커들의 역사적 기록

    model_config = {
        "json_schema_extra": {
            "example": {
                "id": 6,
                "name": "Andrew Blueprint",
            }
        }
    }