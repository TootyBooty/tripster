from db.db import Base
from schemas.publications import PublicationReaction
from schemas.publications import PublicationShow
from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import Enum
from sqlalchemy import ForeignKey
from sqlalchemy import func
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.orm import relationship


class Publication(Base):
    __tablename__ = "publications"

    id = Column(Integer, primary_key=True, autoincrement=True)
    author_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    text = Column(String, nullable=False)
    created_at = Column(DateTime, default=func.now())
    vote_count = Column(Integer, default=0)
    rating = Column(Integer, default=0)

    rated_users = relationship("UserPublicationReact", back_populates="publication")

    def to_read_model(self) -> PublicationShow:
        return PublicationShow(
            id=self.id,
            author_id=self.author_id,
            text=self.text,
            created_at=self.created_at,
            vote_count=self.vote_count,
            rating=self.rating,
        )


class UserPublicationReact(Base):
    __tablename__ = "user_publication_reacts"

    user_id = Column(Integer, ForeignKey("users.id"), primary_key=True)
    publication_id = Column(Integer, ForeignKey("publications.id"), primary_key=True)
    reaction = Column(Enum(PublicationReaction))

    user = relationship("User", back_populates="rated_publications")
    publication = relationship("Publication", back_populates="rated_users")
