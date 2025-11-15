from dataclasses import dataclass

from redis.asyncio import Redis
from sqlalchemy import select

from domain.entities.url import URLEntity
from domain.interfaces.repositories.url import BaseURLRepository
from infrastructure.database.converters.url import (
    convert_url_entity_to_model,
    convert_url_model_to_entity,
)
from infrastructure.database.gateways.postgres import Database
from infrastructure.database.models.url import URLModel


@dataclass
class ComposedURLRepository(BaseURLRepository):
    database: Database
    cache: Redis

    async def add(self, url_pair: URLEntity) -> None:
        short_url = url_pair.short_url
        long_url = url_pair.long_url.as_generic_type()

        model = convert_url_entity_to_model(url_pair)

        async with self.database.get_session() as session:
            session.add(model)
            await session.commit()

        await self.cache.set(short_url, long_url)

    async def get_by_short_url(self, short_url: str) -> str | None:
        cached_long_url = await self.cache.get(short_url)
        if cached_long_url:
            return cached_long_url

        async with self.database.get_read_only_session() as session:
            stmt = select(URLModel).where(URLModel.short_url == short_url)
            result = await session.execute(stmt)
            model = result.scalar_one_or_none()

        if model:
            long_url = model.long_url
            await self.cache.set(short_url, long_url)
            return long_url

        return None

    async def get_by_long_url(self, long_url: str) -> URLEntity | None:
        async with self.database.get_read_only_session() as session:
            stmt = select(URLModel).where(URLModel.long_url == long_url)
            result = await session.execute(stmt)
            model = result.scalar_one_or_none()

        if model:
            return convert_url_model_to_entity(model)
        return None
