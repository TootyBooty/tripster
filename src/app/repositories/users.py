from models.users import User
from repositories.base import SQLAlchemyRepository
from schemas.users import UserShow
from schemas.users import UserShowWithPassword
from sqlalchemy import insert
from sqlalchemy import select


class UserRepository(SQLAlchemyRepository):
    async def create_user(self, data: dict) -> int:
        query = insert(User).values(**data).returning(User.id)
        res = await self.session.execute(query)
        return res.scalar_one()

    async def get_user_by_filter(
        self, _with_password: bool = False, **filter_by
    ) -> UserShow | UserShowWithPassword | None:
        query = select(User).filter_by(**filter_by)
        res = await self.session.execute(query)
        res = res.scalar_one_or_none()
        if res:
            res = res.to_read_model(with_password=_with_password)
        return res
