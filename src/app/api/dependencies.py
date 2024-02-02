from typing import Annotated

from core.config import Config
from core.security import get_user_id_from_token
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from utils.unit_of_work import IUnitOfWork
from utils.unit_of_work import UnitOfWork


UOWDep = Annotated[IUnitOfWork, Depends(UnitOfWork)]


IDFromToken = Annotated[int, Depends(get_user_id_from_token)]
