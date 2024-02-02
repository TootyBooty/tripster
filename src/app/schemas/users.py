import re
from typing import Optional

from fastapi import HTTPException
from pydantic import BaseModel
from pydantic import EmailStr
from pydantic import Field
from pydantic import validator

LETTER_MATCH_PATTERN = re.compile(r"^[а-яА-Яa-zA-Z\-]+$")


class UserCreate(BaseModel):
    name: str = Field(max_length=15)
    email: EmailStr
    password: str

    @validator("name")
    def validate_name(cls, value):
        if not LETTER_MATCH_PATTERN.match(value):
            raise HTTPException(
                status_code=422, detail="Name should contains only letters"
            )
        return value


class UserShow(BaseModel):
    id: int
    name: str = Field(max_length=15)
    email: EmailStr


class UserShowWithPassword(UserShow):
    password: str


class UserGetFilter(BaseModel):
    id: Optional[int] = None
    email: Optional[EmailStr] = None
