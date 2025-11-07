import base62
from dataclasses import dataclass
from domain.entities.url import URLEntity
from domain.interfaces.repositories.url import BaseURLRepository
from domain.exceptions.url import LongURLNotFoundException


@dataclass
class URLService:
    url_repository: BaseURLRepository

    async def get_or_create_short_url(self, long_url: str) -> str:
        existing_pair = await self.url_repository.get_by_long_url(long_url)

        if existing_pair:
            return existing_pair.short_url

        short_url = base62.encode(long_url)

        new_pair = URLEntity(
            long_url=long_url,
            short_url=short_url,
        )

        await self.url_repository.add(new_pair)

        return short_url

    async def get_long_url(self, short_url: str) -> str:
        pair = await self.url_repository.get_by_short_url(short_url)

        if not pair:
            raise LongURLNotFoundException(short_url=short_url)

        return pair.long_url
