from fastapi import (
    FastAPI,
    HTTPException,
    Request,
    status,
)
from fastapi.responses import JSONResponse

from elasticapm import get_client

from domain.exceptions.base import DomainException
from presentation.api.schemas import ApiResponse


def _capture_exception_to_apm(exc: Exception) -> None:
    """Capture exception to Elastic APM."""
    try:
        client = get_client()
        if client:
            client.capture_exception(exc_info=(type(exc), exc, exc.__traceback__))
    except Exception:
        # Silently fail if APM is not configured
        pass


def setup_exception_handlers(app: FastAPI) -> None:
    """Setup exception handlers to return errors in ApiResponse format."""

    @app.exception_handler(DomainException)
    async def domain_exception_handler(
        request: Request,
        exc: DomainException,
    ) -> JSONResponse:
        _capture_exception_to_apm(exc)
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content=ApiResponse(
                data={},
                errors=[exc.message],
            ).model_dump(),
        )

    @app.exception_handler(HTTPException)
    async def http_exception_handler(
        request: Request,
        exc: HTTPException,
    ) -> JSONResponse:
        _capture_exception_to_apm(exc)
        error_message = exc.detail if isinstance(exc.detail, str) else str(exc.detail)
        return JSONResponse(
            status_code=exc.status_code,
            content=ApiResponse(
                data={},
                errors=[error_message],
            ).model_dump(),
        )

    @app.exception_handler(Exception)
    async def general_exception_handler(
        request: Request,
        exc: Exception,
    ) -> JSONResponse:
        _capture_exception_to_apm(exc)
        error_message = str(exc) if str(exc) else "An unexpected error occurred"
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content=ApiResponse(
                data={},
                errors=[error_message],
            ).model_dump(),
        )
