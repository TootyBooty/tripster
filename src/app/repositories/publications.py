from models.publications import Publication
from models.publications import UserPublicationReact
from repositories.base import SQLAlchemyRepository
from sqlalchemy import and_
from sqlalchemy import asc
from sqlalchemy import delete
from sqlalchemy import desc
from sqlalchemy import func
from sqlalchemy import insert
from sqlalchemy import select
from sqlalchemy import update


class PublicationRepository(SQLAlchemyRepository):
    async def add_publication(self, data: dict) -> int:
        query = insert(Publication).values(**data).returning(Publication.id)
        res = await self.session.execute(query)
        return res.scalar_one()

    async def get_publication_list(
        self, limit=10, offset=0, order_by="created_at", ascending=False
    ):

        sort_field = getattr(Publication, order_by, Publication.created_at)

        sort_order = asc(sort_field) if ascending else desc(sort_field)

        query = select(Publication).order_by(sort_order).limit(limit).offset(offset)

        res = await self.session.execute(query)

        res = [row[0].to_read_model() for row in res.all()]
        return res

    async def rate_publication(self, data: dict) -> bool:
        reaction = UserPublicationReact(**data)
        merged = await self.session.merge(reaction)
        return self.session.is_modified(merged)

    async def unrate_publication(self, filter: dict) -> bool:
        conditions = {
            getattr(UserPublicationReact, key) == value for key, value in filter.items()
        }

        query = delete(UserPublicationReact).where(and_(*conditions))
        res = await self.session.execute(query)
        return bool(res.rowcount > 0)

    async def update_publication_rating(self, id: int) -> int:
        subquery = (
            select(
                func.count().label("vote_count"),
                (
                    func.count().filter(UserPublicationReact.reaction == "LIKE")
                    - func.count().filter(UserPublicationReact.reaction == "DISLIKE")
                ).label("rating"),
            )
            .where(UserPublicationReact.publication_id == id)
            .correlate_except(Publication)
        )

        query = (
            update(Publication)
            .values({"rating": subquery.c.rating, "vote_count": subquery.c.vote_count})
            .filter_by(id=id)
            .returning(Publication.rating)
        )

        res = await self.session.execute(query)

        return res.scalar_one_or_none()
