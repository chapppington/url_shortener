import pytest
from faker import Faker

from application.commands.url import CreateShortURLCommand
from application.mediator import Mediator
from application.queries.url import GetLongURLQuery
from domain.exceptions.url import (
    EmptyURLError,
    InvalidURLError,
    LongURLNotFoundException,
    URLTooLongError,
)
from domain.interfaces.repositories.url import BaseURLRepository
from domain.value_objects.url import MAX_URL_LENGTH


@pytest.mark.asyncio
async def test_create_short_url_command_success(
    url_repository: BaseURLRepository,
    mediator: Mediator,
    faker: Faker,
):
    long_url = faker.url()
    results = await mediator.handle_command(CreateShortURLCommand(long_url=long_url))
    short_url = results[0]

    assert short_url is not None
    assert isinstance(short_url, str)

    entity = await url_repository.get_by_long_url(long_url)
    assert entity is not None
    assert entity.long_url.value == long_url
    assert entity.short_url == short_url


@pytest.mark.asyncio
async def test_create_short_url_command_returns_existing(
    mediator: Mediator,
    faker: Faker,
):
    long_url = faker.url()

    results1 = await mediator.handle_command(CreateShortURLCommand(long_url=long_url))
    short_url1 = results1[0]

    results2 = await mediator.handle_command(CreateShortURLCommand(long_url=long_url))
    short_url2 = results2[0]

    assert short_url1 == short_url2


@pytest.mark.asyncio
async def test_get_long_url_query_success(
    mediator: Mediator,
    faker: Faker,
):
    long_url = faker.url()

    create_results = await mediator.handle_command(
        CreateShortURLCommand(long_url=long_url),
    )
    short_url = create_results[0]

    retrieved_long_url = await mediator.handle_query(
        GetLongURLQuery(short_url=short_url),
    )

    assert retrieved_long_url == long_url
    assert isinstance(retrieved_long_url, str)


@pytest.mark.asyncio
async def test_get_long_url_query_not_found(
    mediator: Mediator,
):
    non_existent_short_url = "nonexistent123"

    with pytest.raises(LongURLNotFoundException):
        await mediator.handle_query(GetLongURLQuery(short_url=non_existent_short_url))


@pytest.mark.asyncio
async def test_multiple_different_urls(
    mediator: Mediator,
    faker: Faker,
):
    urls = [faker.url() for _ in range(3)]
    short_urls = []

    for long_url in urls:
        results = await mediator.handle_command(
            CreateShortURLCommand(long_url=long_url),
        )
        short_url = results[0]
        short_urls.append(short_url)

        retrieved = await mediator.handle_query(GetLongURLQuery(short_url=short_url))
        assert retrieved == long_url
        assert isinstance(retrieved, str)

    assert len(set(short_urls)) == len(short_urls)


@pytest.mark.asyncio
async def test_create_short_url_command_invalid_url_empty(
    mediator: Mediator,
):
    """Test that empty URL raises validation error."""
    with pytest.raises(EmptyURLError):
        await mediator.handle_command(CreateShortURLCommand(long_url=""))


@pytest.mark.asyncio
async def test_create_short_url_command_invalid_url_no_scheme(
    mediator: Mediator,
):
    """Test that URL without scheme raises validation error."""
    with pytest.raises(InvalidURLError):
        await mediator.handle_command(CreateShortURLCommand(long_url="example.com"))


@pytest.mark.asyncio
async def test_create_short_url_command_invalid_url_unsupported_scheme(
    mediator: Mediator,
):
    """Test that URL with unsupported scheme raises validation error."""
    with pytest.raises(InvalidURLError):
        await mediator.handle_command(
            CreateShortURLCommand(long_url="ftp://example.com"),
        )


@pytest.mark.asyncio
async def test_create_short_url_command_invalid_url_too_long(
    mediator: Mediator,
):
    """Test that URL exceeding max length raises validation error."""
    long_url = "https://example.com/" + "a" * (MAX_URL_LENGTH + 1)

    with pytest.raises(URLTooLongError):
        await mediator.handle_command(CreateShortURLCommand(long_url=long_url))
