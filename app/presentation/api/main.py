from fastapi import FastAPI

from presentation.api.healthcheck import healthcheck_router


def create_app() -> FastAPI:
    app = FastAPI(
        title="URL Shortener",
        description="URL Shortener",
        docs_url="/api/docs",
        debug=True,
    )

    app.include_router(healthcheck_router)

    return app
