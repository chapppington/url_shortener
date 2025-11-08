from dataclasses import dataclass
from uuid import uuid4

import base62

from domain.entities.url import URLEntity
from domain.exceptions.url import LongURLNotFoundException
from domain.interfaces.repositories.url import BaseURLRepository
from domain.value_objects.url import LongURLValueObject


@dataclass
class URLService:
    url_repository: BaseURLRepository

    async def get_or_create_short_url(self, long_url: str) -> str:
        existing_pair = await self.url_repository.get_by_long_url(long_url)

        if existing_pair:
            return existing_pair.short_url

        new_id = uuid4()

        # Просто используем числовое представление UUID (обрезаем если нужно)
        numeric_value = new_id.int & ((1 << 48) - 1)  # Берем младшие 48 бит

        # Кодируем в base62
        short_url = base62.encode(numeric_value)

        new_pair = URLEntity(
            id=new_id,
            long_url=LongURLValueObject(value=long_url),
            short_url=short_url,
        )

        await self.url_repository.add(new_pair)

        return short_url

    async def get_long_url(self, short_url: str) -> str:
        long_url = await self.url_repository.get_by_short_url(short_url)

        if not long_url:
            raise LongURLNotFoundException(short_url=short_url)

        return long_url
