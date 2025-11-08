from dataclasses import dataclass

from redis.asyncio import Redis
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from domain.entities.url import URLEntity
from domain.interfaces.repositories.url import BaseURLRepository
from infrastructure.database.converters.url import (
    convert_url_entity_to_model,
    convert_url_model_to_entity,
)
from infrastructure.database.models.url import URLModel


@dataclass
class ComposedURLRepository(BaseURLRepository):
    db_session: AsyncSession
    cache: Redis

    async def add(self, url_pair: URLEntity) -> None:
        # Сохраняем значения до commit, чтобы избежать lazy loading после detach
        short_url = url_pair.short_url
        long_url = url_pair.long_url.as_generic_type()

        # Добавляем в бд
        model = convert_url_entity_to_model(url_pair)
        self.db_session.add(model)
        await self.db_session.commit()

        # Добавляем в кэш
        await self.cache.set(short_url, long_url)

    async def get_by_short_url(self, short_url: str) -> str | None:
        cached_long_url = await self.cache.get(short_url)

        if cached_long_url:
            return cached_long_url

        stmt = select(URLModel).where(URLModel.short_url == short_url)
        result = await self.db_session.execute(stmt)
        model = result.scalar_one_or_none()

        if model:
            # Используем прямое обращение к атрибуту, так как модель уже загружена
            long_url = model.long_url
            await self.cache.set(short_url, long_url)
            return long_url

        return None

    async def get_by_long_url(self, long_url: str) -> URLEntity | None:
        # Ищем в БД по long_url
        stmt = select(URLModel).where(URLModel.long_url == long_url)
        result = await self.db_session.execute(stmt)
        model = result.scalar_one_or_none()

        if model:
            return convert_url_model_to_entity(model)

        return None
