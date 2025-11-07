from dataclasses import (
    dataclass,
    field,
)

from domain.entities.url import URLEntity
from domain.interfaces.repositories.url import BaseURLRepository


@dataclass
class DummyInMemoryURLRepository(BaseURLRepository):
    _url_pairs: list[URLEntity] = field(default_factory=list, kw_only=True)

    async def add(self, url_pair: URLEntity) -> None:
        self._url_pairs.append(url_pair)

    async def get_by_short_url(self, short_url: str) -> URLEntity | None:
        try:
            return next(
                url_pair
                for url_pair in self._url_pairs
                if url_pair.short_url == short_url
            )
        except StopIteration:
            return None
