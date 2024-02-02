from db.db import Base
from schemas.users import UserShow
from schemas.users import UserShowWithPassword
from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.orm import relationship


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String(50), unique=True)
    name = Column(String(15))
    password = Column(String)

    rated_publications = relationship("UserPublicationReact", back_populates="user")

    def to_read_model(self, with_password=False) -> UserShow | UserShowWithPassword:
        if with_password:
            return UserShowWithPassword(
                id=self.id, name=self.name, email=self.email, password=self.password
            )
        return UserShow(
            id=self.id,
            name=self.name,
            email=self.email,
        )
