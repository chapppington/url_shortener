from fastapi import FastAPI
from fastapi.testclient import TestClient

import pytest
from punq import Container

from application.init import init_container
from presentation.api.main import create_app
from tests.fixtures import init_dummy_container


@pytest.fixture
def container() -> Container:
    return init_dummy_container()


@pytest.fixture
def app(container: Container) -> FastAPI:
    app = create_app()
    app.dependency_overrides[init_container] = lambda: container

    return app


@pytest.fixture
def client(app: FastAPI) -> TestClient:
    return TestClient(app=app)
