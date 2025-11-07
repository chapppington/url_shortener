from punq import Container
from pytest import fixture

from application.mediator import Mediator
from domain.interfaces.repositories.url import BaseURLRepository
from tests.fixtures import init_dummy_container


@fixture(scope="function")
def container() -> Container:
    return init_dummy_container()


@fixture()
def mediator(container: Container) -> Mediator:
    return container.resolve(Mediator)


@fixture()
def url_repository(container: Container) -> BaseURLRepository:
    return container.resolve(BaseURLRepository)
