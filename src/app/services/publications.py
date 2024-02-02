from exceptions import PublicatonNotFound
from schemas.publications import PublicationCreate
from schemas.publications import PublicationListFilter
from schemas.publications import PublicationRate
from schemas.publications import PublicationUnrate
from sqlalchemy.exc import IntegrityError
from utils.unit_of_work import IUnitOfWork


class PublicationService:
    async def create_publication(
        self, uow: IUnitOfWork, publication_data: PublicationCreate
    ) -> int:
        publication_dict = publication_data.model_dump()
        async with uow:
            publication_id = await uow.publications.add_publication(publication_dict)
            await uow.commit()
            return publication_id

    async def get_publications(self, uow: IUnitOfWork, filter: PublicationListFilter):
        publication_filter = filter.model_dump(exclude_none=True)
        async with uow:
            publications = await uow.publications.get_publication_list(
                **publication_filter
            )
            return publications

    async def rate_publication(
        self, uow: IUnitOfWork, publication_rate: PublicationRate
    ) -> bool:
        publication_dict = publication_rate.model_dump()

        async with uow:
            try:
                is_modified = await uow.publications.rate_publication(publication_dict)

                if is_modified:
                    await uow.publications.update_publication_rating(
                        id=publication_rate.publication_id
                    )

            except IntegrityError:
                raise PublicatonNotFound

            await uow.commit()
            return is_modified

    async def unrate_publication(
        self, uow: IUnitOfWork, unrate_filter: PublicationUnrate
    ):
        unrate_filter_dict = unrate_filter.model_dump()

        async with uow:
            is_deleted = await uow.publications.unrate_publication(
                filter=unrate_filter_dict
            )
            if is_deleted:
                await uow.publications.update_publication_rating(
                    id=unrate_filter.publication_id
                )
            await uow.commit()
            return is_deleted
