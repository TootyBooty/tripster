import hashlib
from datetime import datetime
from datetime import timedelta
from typing import Optional

from core.config import Config
from exceptions import CredentialsException
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from jose import JWTError

oauth2_scheme = OAuth2PasswordBearer(tokenUrl=Config.TOKEN_URL)


def get_password_hash(password: str) -> bool:
    sha256 = hashlib.sha256()
    sha256.update(password.encode("utf-8"))
    hashed_password = sha256.hexdigest()
    return hashed_password


def verify_password(plain_password: str, hashed_password: str) -> bool:
    sha256 = hashlib.sha256()
    sha256.update(plain_password.encode("utf-8"))
    hashed_password_to_check = sha256.hexdigest()
    return hashed_password == hashed_password_to_check


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(
            minutes=Config.ACCESS_TOKEN_EXPIRE_MINUTES
        )
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, Config.SECRET_KEY, algorithm=Config.ALGORITHM)
    return encoded_jwt


async def get_user_id_from_token(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, Config.SECRET_KEY, algorithms=[Config.ALGORITHM])
        user_id: int = int(payload.get("sub"))
        if not user_id:
            raise CredentialsException
    except JWTError:
        raise CredentialsException
    return user_id
