from pydantic import BaseModel


class AndrewBlueprintSchema(BaseModel):
    id: int = 1
    name: str = "andrew"
    memo: str = "앤드류는 타이타닉의 승무원이다"
