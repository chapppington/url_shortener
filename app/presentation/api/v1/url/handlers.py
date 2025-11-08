from fastapi import (
    APIRouter,
    Depends,
    status,
)

from application.commands.url import CreateShortURLCommand
from application.init import init_container
from application.mediator import Mediator
from application.queries.url import GetLongURLQuery
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

    results = await mediator.handle_command(command)
    short_url = results[0]

    return ApiResponse[CreateShortURLResponseSchema](
        data=CreateShortURLResponseSchema(short_url=short_url),
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

    long_url = await mediator.handle_query(query)

    return ApiResponse[GetLongURLResponseSchema](
        data=GetLongURLResponseSchema(long_url=long_url),
    )
