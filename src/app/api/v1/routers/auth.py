from api.dependencies import UOWDep
from fastapi import APIRouter
from fastapi import Depends
from fastapi.security import OAuth2PasswordRequestForm
from schemas.auth import Token
from schemas.users import UserCreate
from schemas.users import UserGetFilter
from services.users import UserService


auth_router = APIRouter()


@auth_router.post("/register")
async def register(
    user: UserCreate,
    uow: UOWDep,
) -> int:
    user_id = await UserService().create_user(uow, user)
    return {"user_id": user_id}


@auth_router.post("/token")
async def token_login(
    uow: UOWDep,
    form_data: OAuth2PasswordRequestForm = Depends(),
) -> Token:
    token = await UserService().token_login(
        uow, UserGetFilter(email=form_data.username), form_data.password
    )

    return token
