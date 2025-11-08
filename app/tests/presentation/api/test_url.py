from fastapi import (
    FastAPI,
    status,
)
from fastapi.testclient import TestClient

import pytest
from faker import Faker
from httpx import Response

from domain.value_objects.url import MAX_URL_LENGTH


@pytest.mark.asyncio
async def test_create_short_url_success(
    app: FastAPI,
    client: TestClient,
    faker: Faker,
):
    url = app.url_path_for("create_short_url")
    long_url = faker.url()
    response: Response = client.post(url=url, json={"long_url": long_url})

    assert response.status_code == status.HTTP_201_CREATED
    json_response = response.json()

    assert "data" in json_response
    assert "short_url" in json_response["data"]
    assert isinstance(json_response["data"]["short_url"], str)
    assert len(json_response["data"]["short_url"]) > 0


@pytest.mark.asyncio
async def test_create_short_url_returns_existing(
    app: FastAPI,
    client: TestClient,
    faker: Faker,
):
    url = app.url_path_for("create_short_url")
    long_url = faker.url()

    response1: Response = client.post(url=url, json={"long_url": long_url})
    assert response1.status_code == status.HTTP_201_CREATED
    short_url1 = response1.json()["data"]["short_url"]

    response2: Response = client.post(url=url, json={"long_url": long_url})
    assert response2.status_code == status.HTTP_201_CREATED
    short_url2 = response2.json()["data"]["short_url"]

    assert short_url1 == short_url2


@pytest.mark.asyncio
async def test_get_long_url_success(
    app: FastAPI,
    client: TestClient,
    faker: Faker,
):
    create_url = app.url_path_for("create_short_url")
    long_url = faker.url()

    create_response: Response = client.post(
        url=create_url,
        json={"long_url": long_url},
    )
    assert create_response.status_code == status.HTTP_201_CREATED
    short_url = create_response.json()["data"]["short_url"]

    get_url = app.url_path_for("get_long_url", short_url=short_url)
    get_response: Response = client.get(url=get_url)

    assert get_response.status_code == status.HTTP_200_OK
    json_response = get_response.json()

    assert "data" in json_response
    assert "long_url" in json_response["data"]
    assert json_response["data"]["long_url"] == long_url


@pytest.mark.asyncio
async def test_get_long_url_not_found(
    app: FastAPI,
    client: TestClient,
):
    non_existent_short_url = "nonexistent123"
    get_url = app.url_path_for("get_long_url", short_url=non_existent_short_url)
    response: Response = client.get(url=get_url)

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    json_response = response.json()
    assert "errors" in json_response
    assert isinstance(json_response["errors"], list)
    assert len(json_response["errors"]) > 0


@pytest.mark.asyncio
async def test_create_short_url_invalid_empty_url(
    app: FastAPI,
    client: TestClient,
):
    """Test that empty URL returns 400 Bad Request."""
    url = app.url_path_for("create_short_url")
    response: Response = client.post(url=url, json={"long_url": ""})

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    json_response = response.json()
    assert "errors" in json_response
    assert isinstance(json_response["errors"], list)
    assert len(json_response["errors"]) > 0
    error_message = json_response["errors"][0].lower()
    assert "empty" in error_message or "cannot be empty" in error_message


@pytest.mark.asyncio
async def test_create_short_url_invalid_url_no_scheme(
    app: FastAPI,
    client: TestClient,
):
    """Test that URL without scheme returns 400 Bad Request."""
    url = app.url_path_for("create_short_url")
    response: Response = client.post(url=url, json={"long_url": "example.com"})

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    json_response = response.json()
    assert "errors" in json_response
    assert isinstance(json_response["errors"], list)
    assert len(json_response["errors"]) > 0
    assert "scheme" in json_response["errors"][0].lower()


@pytest.mark.asyncio
async def test_create_short_url_invalid_url_unsupported_scheme(
    app: FastAPI,
    client: TestClient,
):
    """Test that URL with unsupported scheme returns 400 Bad Request."""
    url = app.url_path_for("create_short_url")
    response: Response = client.post(url=url, json={"long_url": "ftp://example.com"})

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    json_response = response.json()
    assert "errors" in json_response
    assert isinstance(json_response["errors"], list)
    assert len(json_response["errors"]) > 0
    error_message = json_response["errors"][0].lower()
    assert "unsupported" in error_message or "only http and https" in error_message


@pytest.mark.asyncio
async def test_create_short_url_invalid_url_too_long(
    app: FastAPI,
    client: TestClient,
):
    """Test that URL exceeding max length returns 400 Bad Request."""
    url = app.url_path_for("create_short_url")
    long_url = "https://example.com/" + "a" * (MAX_URL_LENGTH + 1)
    response: Response = client.post(url=url, json={"long_url": long_url})

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    json_response = response.json()
    assert "errors" in json_response
    assert isinstance(json_response["errors"], list)
    assert len(json_response["errors"]) > 0
    assert "too long" in json_response["errors"][0].lower()
