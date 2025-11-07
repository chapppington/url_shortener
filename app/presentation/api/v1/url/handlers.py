from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status,
)

from application.commands.url import CreateShortURLCommand
from application.init import init_container
from application.mediator import Mediator
from application.queries.url import GetLongURLQuery
from domain.exceptions.url import LongURLNotFoundException
from presentation.api.schemas import ApiResponse
from presentation.api.v1.url.schemas import (
    CreateShortURLRequestSchema,
    CreateShortURLResponseSchema,
    GetLongURLResponseSchema,
)


router = APIRouter(prefix="/urls", tags=["urls"])


@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    response_model=ApiResponse[CreateShortURLResponseSchema],
    responses={
        status.HTTP_201_CREATED: {"model": ApiResponse[CreateShortURLResponseSchema]},
        status.HTTP_400_BAD_REQUEST: {"model": ApiResponse},
    },
)
async def create_short_url(
    request: CreateShortURLRequestSchema,
    container=Depends(init_container),
) -> ApiResponse[CreateShortURLResponseSchema]:
    mediator: Mediator = container.resolve(Mediator)
    command = CreateShortURLCommand(long_url=request.long_url)

    try:
        results = await mediator.handle_command(command)
        short_url = results[0]

        return ApiResponse[CreateShortURLResponseSchema](
            data=CreateShortURLResponseSchema(short_url=short_url),
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )


@router.get(
    "/{short_url}",
    status_code=status.HTTP_200_OK,
    response_model=ApiResponse[GetLongURLResponseSchema],
    responses={
        status.HTTP_200_OK: {"model": ApiResponse[GetLongURLResponseSchema]},
        status.HTTP_400_BAD_REQUEST: {"model": ApiResponse},
    },
)
async def get_long_url(
    short_url: str,
    container=Depends(init_container),
) -> ApiResponse[GetLongURLResponseSchema]:
    mediator: Mediator = container.resolve(Mediator)
    query = GetLongURLQuery(short_url=short_url)

    try:
        long_url = await mediator.handle_query(query)

        return ApiResponse[GetLongURLResponseSchema](
            data=GetLongURLResponseSchema(long_url=long_url),
        )
    except LongURLNotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=e.message,
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )
