from pydantic import BaseModel, Field


class SmithCaptainResponseSchema(BaseModel):

    id: int
    name: str


class ChatSchema(BaseModel):

    id: int = Field(0, description="Captain ID")
    name: str = Field("에드워드 스미스", description="Captain's name")
    # 타이타닉 선장. 백만장자들의 선장이라 불렸으며 고조되는 위기 속에 배와 운명을 함께함

    model_config = {
        "json_schema_extra": {
            "example": {
                "id": 5,
                "name": "Edward Smith",
                "messages": "탑승객이 몇 명이야?",
            }
        }
    }


class SmithCaptainChatRequestSchema(BaseModel):
    message: str = Field(..., min_length=1, description="사용자가 입력한 자연어")


class SmithCaptainChatResponseSchema(BaseModel):
    answer: str
