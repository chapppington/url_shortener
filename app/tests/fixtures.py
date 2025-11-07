from punq import (
    Container,
    Scope,
)

from application.init import _init_container
from domain.interfaces.repositories.url import BaseURLRepository
from infrastructure.database.repositories.url.memory import DummyInMemoryURLRepository


def init_dummy_container() -> Container:
    container = _init_container()

    container.register(
        BaseURLRepository,
        DummyInMemoryURLRepository,
        scope=Scope.singleton,
    )

    return container
