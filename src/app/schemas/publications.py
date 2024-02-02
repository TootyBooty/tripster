import enum
from datetime import datetime
from typing import Optional

from pydantic import BaseModel
from pydantic import Field


class PublicationIn(BaseModel):
    text: str = Field(max_length=5000)


class PublicationCreate(PublicationIn):
    author_id: int


class PublicationShow(BaseModel):
    id: int
    author_id: int
    text: str
    created_at: datetime
    vote_count: int
    rating: int


class PublicationListFilter(BaseModel):
    limit: Optional[int] = Field(ge=1, le=100, default=None)
    offset: Optional[int] = Field(ge=0, default=None)
    order_by: Optional[str] = None
    ascending: Optional[bool] = None


class PublicationReaction(str, enum.Enum):
    LIKE = "like"
    DISLIKE = "dislike"


class PublicationUnrate(BaseModel):
    user_id: int
    publication_id: int


class PublicationRate(PublicationUnrate):
    reaction: PublicationReaction
