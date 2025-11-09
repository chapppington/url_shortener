from functools import lru_cache

from punq import (
    Container,
    Scope,
)
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import (
    async_sessionmaker,
    AsyncSession,
    create_async_engine,
)

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
from infrastructure.database.repositories.url.composed import ComposedURLRepository
from settings.config import Config


@lru_cache(1)
def init_container():
    return _init_container()


def _init_container() -> Container:
    container = Container()

    container.register(Config, instance=Config(), scope=Scope.singleton)

    container.register(URLService)  # убрал тут синглтон

    # один раз создаём async_sessionmaker
    def init_async_sessionmaker():
        config: Config = container.resolve(Config)
        engine = create_async_engine(config.postgres_connection_uri, echo=False)
        return async_sessionmaker[AsyncSession](bind=engine, expire_on_commit=False)

    container.register(
        async_sessionmaker,
        factory=init_async_sessionmaker,
        scope=Scope.singleton,
    )

    # один раз создаём redis клиент
    def init_redis_client():
        config: Config = container.resolve(Config)
        return Redis(
            host=config.redis_host,
            port=config.redis_port,
            decode_responses=True,
        )

    container.register(Redis, factory=init_redis_client, scope=Scope.singleton)

    def init_url_repository():
        sessionmaker: async_sessionmaker[AsyncSession] = container.resolve(
            async_sessionmaker,
        )
        redis_client = container.resolve(Redis)
        return ComposedURLRepository(sessionmaker=sessionmaker, cache=redis_client)

    container.register(
        BaseURLRepository,
        factory=init_url_repository,  # убрал тут синглтон
    )

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
    )  # тут добавил синглтон

    return container
