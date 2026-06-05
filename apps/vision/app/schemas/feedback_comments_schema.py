from datetime import datetime

from pydantic import BaseModel, Field


class FeedbackCommentNestedCreateRequest(BaseModel):
    user_id: int
    parent_comment_id: int | None = None
    body: str = Field(..., min_length=1, max_length=2000)


class FeedbackCommentResponse(BaseModel):
    id: int
    feedback_id: int
    user_id: int
    parent_comment_id: int | None
    body: str
    created_at: datetime

    model_config = {"from_attributes": True}
