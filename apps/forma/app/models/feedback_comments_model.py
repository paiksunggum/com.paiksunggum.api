from datetime import datetime

from sqlmodel import Field, SQLModel

from .model_utils import now_utc


class FeedbackComment(SQLModel, table=True):
    __tablename__ = "feedback_comments"

    id: int | None = Field(
        default=None,
        primary_key=True,
        sa_column_kwargs={"name": "id"},
    )
    feedback_id: int = Field(foreign_key="feedbacks.id", index=True)
    user_id: int = Field(foreign_key="users.id", index=True)
    parent_comment_id: int | None = Field(
        default=None,
        foreign_key="feedback_comments.id",
        index=True,
    )
    body: str = Field(max_length=2000)
    created_at: datetime = Field(default_factory=now_utc)
