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

    container.register(URLService, scope=Scope.singleton)

    def init_url_repository():
        config: Config = container.resolve(Config)

        # PostgreSQL session
        async_engine = create_async_engine(config.postgres_connection_uri, echo=True)
        async_session_factory = async_sessionmaker[AsyncSession](bind=async_engine)

        postgres_session = async_session_factory()

        # Redis client
        redis_client = Redis(
            host=config.redis_host,
            port=config.redis_port,
            decode_responses=True,
        )

        return ComposedURLRepository(db_session=postgres_session, cache=redis_client)

    container.register(
        BaseURLRepository,
        factory=init_url_repository,
        scope=Scope.singleton,
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

    container.register(Mediator, factory=init_mediator)

    return container
