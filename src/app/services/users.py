from core.security import create_access_token
from core.security import get_password_hash
from core.security import verify_password
from exceptions import CredentialsException
from exceptions import EmailAlreadyTaken
from exceptions import UserNotFound
from schemas.auth import Token
from schemas.users import UserCreate
from schemas.users import UserGetFilter
from schemas.users import UserShow
from sqlalchemy.exc import IntegrityError
from utils.unit_of_work import IUnitOfWork


class UserService:
    async def create_user(self, uow: IUnitOfWork, user: UserCreate) -> int:
        user_dict = user.model_dump(exclude_none=True)
        user_dict["password"] = get_password_hash(user.password)
        async with uow:
            try:
                user_id = await uow.users.create_user(user_dict)
            except IntegrityError:
                raise EmailAlreadyTaken
            await uow.commit()
            return user_id

    async def get_user(self, uow: IUnitOfWork, filter: UserGetFilter) -> UserShow:
        user_filter = filter.model_dump(exclude_none=True)
        async with uow:
            user = await uow.users.get_user_by_filter(**user_filter)
            if not user:
                raise UserNotFound
            return user

    async def token_login(
        self, uow: IUnitOfWork, filter: UserGetFilter, input_password: str
    ):
        user_filter = filter.model_dump(exclude_none=True)

        async with uow:
            user_with_password = await uow.users.get_user_by_filter(
                _with_password=True, **user_filter
            )

        if user_with_password is None:
            raise CredentialsException

        if not verify_password(input_password, user_with_password.password):
            raise CredentialsException

        access_token = create_access_token(data={"sub": str(user_with_password.id)})

        return Token(access_token=access_token, token_type="bearer")
