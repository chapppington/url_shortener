import pytest
from faker import Faker

from application.commands.url import CreateShortURLCommand
from application.mediator import Mediator
from application.queries.url import GetLongURLQuery
from domain.exceptions.url import LongURLNotFoundException
from domain.interfaces.repositories.url import BaseURLRepository


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
    assert entity.long_url == long_url
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

    assert len(set(short_urls)) == len(short_urls)
