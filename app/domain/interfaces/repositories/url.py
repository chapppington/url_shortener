from abc import (
    ABC,
    abstractmethod,
)

from domain.entities.url import URLEntity


class BaseURLRepository(ABC):
    @abstractmethod
    async def add(self, url_pair: URLEntity) -> None: ...

    @abstractmethod
    async def get_by_short_url(self, short_url: str) -> URLEntity | None: ...
