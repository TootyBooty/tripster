from typing import Annotated

from api.dependencies import IDFromToken
from api.dependencies import UOWDep
from fastapi import APIRouter
from fastapi import Body
from fastapi import Path
from fastapi import Query
from schemas.publications import PublicationCreate
from schemas.publications import PublicationIn
from schemas.publications import PublicationListFilter
from schemas.publications import PublicationRate
from schemas.publications import PublicationReaction
from schemas.publications import PublicationShow
from schemas.publications import PublicationUnrate
from services.publications import PublicationService


publications_router = APIRouter()


@publications_router.get("/")
async def get_publication_list(
    uow: UOWDep,
    limit: Annotated[int | None, Query(ge=1, le=100)] = None,
    offset: Annotated[int | None, Query(ge=0)] = None,
    order_by: Annotated[str | None, Query(example="created_at")] = None,
    ascending: Annotated[bool | None, Query(example=True)] = None,
) -> list[PublicationShow]:
    publications_filter = PublicationListFilter(
        limit=limit, offset=offset, order_by=order_by, ascending=ascending
    )
    publications = await PublicationService().get_publications(
        uow, filter=publications_filter
    )
    return publications


@publications_router.post("/")
async def create_publication(
    publication: PublicationIn,
    author_id: IDFromToken,
    uow: UOWDep,
) -> int:
    publication_data = PublicationCreate(
        **publication.model_dump(), author_id=author_id
    )
    publication_id = await PublicationService().create_publication(
        uow, publication_data
    )
    return {"publication_id": publication_id}


@publications_router.post("/{publication_id}/rate")
async def rate_publication(
    user_id: IDFromToken,
    uow: UOWDep,
    publication_id: int = Path(),
    reaction: PublicationReaction = Body(),
) -> bool:
    publication_rate = PublicationRate(
        user_id=user_id, publication_id=publication_id, reaction=reaction
    )
    is_rated = await PublicationService().rate_publication(uow, publication_rate)
    return {"publication rated": is_rated}


@publications_router.delete("/{publication_id}/rate")
async def unrate_publication(
    user_id: IDFromToken,
    uow: UOWDep,
    publication_id: int = Path(),
) -> bool:
    unrate_filter = PublicationUnrate(user_id=user_id, publication_id=publication_id)
    is_unrated = await PublicationService().unrate_publication(uow, unrate_filter)
    return {"publication unrated": is_unrated}
