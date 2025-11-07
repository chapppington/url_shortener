from fastapi import FastAPI

from presentation.api.healthcheck import healthcheck_router
from presentation.api.v1 import v1_router


def create_app() -> FastAPI:
    app = FastAPI(
        title="URL Shortener",
        description="URL Shortener",
        docs_url="/api/docs",
        debug=True,
    )

    app.include_router(healthcheck_router)
    app.include_router(v1_router, prefix="/api/v1")
    return app
