from dataclasses import dataclass

from application.queries.base import (
    BaseQuery,
    BaseQueryHandler,
)
from domain.services.url import URLService


@dataclass(frozen=True)
class GetLongURLQuery(BaseQuery):
    short_url: str


@dataclass(frozen=True)
class GetLongURLQueryHandler(
    BaseQueryHandler[GetLongURLQuery, str],
):
    url_service: URLService

    async def handle(self, query: GetLongURLQuery) -> str:
        long_url = await self.url_service.get_long_url(
            short_url=query.short_url,
        )
        return long_url
