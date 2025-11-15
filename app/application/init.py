from functools import lru_cache

from punq import (
    Container,
    Scope,
)
from redis.asyncio import Redis

from application.commands.url import (
    CreateShortURLCommand,
    CreateShortURLCommandHandler,
)
from application.mediator import Mediator
from application.queries.url import (
    GetLongURLQuery,
    GetLongURLQueryHandler,
)
from domain.interfaces.repositories.url import BaseURLRepository
from domain.services.url import URLService
from infrastructure.database.gateways.postgres import Database
from infrastructure.database.repositories.url import SQLAlchemyRedisURLRepository
from settings.config import Config


@lru_cache(1)
def init_container():
    return _init_container()


def _init_container() -> Container:
    container = Container()

    container.register(Config, instance=Config(), scope=Scope.singleton)

    def init_database():
        config: Config = container.resolve(Config)
        return Database(
            url=config.postgres_connection_uri,
            ro_url=config.postgres_connection_uri,
        )

    container.register(Database, factory=init_database, scope=Scope.singleton)

    def init_redis():
        config: Config = container.resolve(Config)
        return Redis(
            host=config.redis_host,
            port=config.redis_port,
            decode_responses=True,
        )

    container.register(Redis, factory=init_redis, scope=Scope.singleton)

    container.register(BaseURLRepository, SQLAlchemyRedisURLRepository)

    container.register(URLService)

    container.register(CreateShortURLCommandHandler)
    container.register(GetLongURLQueryHandler)

    def init_mediator():
        mediator = Mediator()

        mediator.register_command(
            CreateShortURLCommand,
            [container.resolve(CreateShortURLCommandHandler)],
        )
        mediator.register_query(
            GetLongURLQuery,
            container.resolve(GetLongURLQueryHandler),
        )

        return mediator

    container.register(
        Mediator,
        factory=init_mediator,
        scope=Scope.singleton,
    )

    return container
