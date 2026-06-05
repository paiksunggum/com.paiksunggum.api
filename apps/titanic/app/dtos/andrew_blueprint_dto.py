from dataclasses import dataclass


@dataclass
class AndrewBlueprintQuery:
    id: int = 1
    name: str = "andrew"
    memo: str = "앤드류는 타이타닉의 승무원이다"



@dataclass
class AndrewBlueprintResponse:
    id: int
    name: str
    memo: str