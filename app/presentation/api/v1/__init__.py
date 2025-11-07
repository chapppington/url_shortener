from fastapi import APIRouter

from presentation.api.v1.url.handlers import router as url_router


v1_router = APIRouter()

v1_router.include_router(url_router)
