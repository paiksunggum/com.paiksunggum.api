from dataclasses import dataclass


@dataclass(frozen=True) # 생성 후 수정 불가하도록 설정
class AndrewBlueprintQuery:
    id: int   # 직관적인 타입 변경
    name: str = "andrew"
    memo: str = "앤드류는 타이타닉의 승무원이다"



@dataclass(frozen=True) # 생성 후 수정 불가하도록 설정
class AndrewBlueprintResponse:
    id: int   # 직관적인 타입 변경
    name: str
    memo: str