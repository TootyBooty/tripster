from api.v1.routers.auth import auth_router
from api.v1.routers.publications import publications_router
from fastapi import APIRouter


v1_router = APIRouter(prefix="/api/v1")

v1_router.include_router(auth_router, prefix="/auth", tags=["auth"])
v1_router.include_router(
    publications_router, prefix="/publication", tags=["publication"]
)
