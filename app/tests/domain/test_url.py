from datetime import datetime
from uuid import uuid4

import pytest

from domain.entities.url import URLEntity


@pytest.mark.parametrize(
    "long_url,short_url,should_succeed",
    [
        ("https://example.com", "abc123", True),
        ("https://google.com", "xyz789", True),
        ("", "abc123", True),
        ("https://example.com", "", True),
    ],
)
def test_create_url_entity(long_url, short_url, should_succeed):
    if should_succeed:
        entity = URLEntity(
            long_url=long_url,
            short_url=short_url,
        )
        assert entity.long_url == long_url
        assert entity.short_url == short_url
        assert entity.id is not None
        assert entity.created_at.date() == datetime.today().date()
        assert entity.updated_at.date() == datetime.today().date()


def test_create_url_entity_with_custom_id():
    entity_id = uuid4()
    entity = URLEntity(
        id=entity_id,
        long_url="https://example.com",
        short_url="abc123",
    )

    assert entity.id == entity_id
    assert entity.long_url == "https://example.com"
    assert entity.short_url == "abc123"


def test_url_entity_equality_by_short_url():
    entity1 = URLEntity(
        long_url="https://example.com",
        short_url="abc123",
    )

    entity2 = URLEntity(
        long_url="https://different.com",
        short_url="abc123",
    )

    assert entity1 == entity2
    assert hash(entity1) == hash(entity2)


def test_url_entity_inequality_by_different_short_url():
    entity1 = URLEntity(
        long_url="https://example.com",
        short_url="abc123",
    )

    entity2 = URLEntity(
        long_url="https://example.com",
        short_url="xyz789",
    )

    assert entity1 != entity2
    assert hash(entity1) != hash(entity2)


def test_url_entity_uniqueness_by_short_url():
    short_url = "unique123"

    entity1 = URLEntity(
        id=uuid4(),
        long_url="https://example.com",
        short_url=short_url,
    )

    entity2 = URLEntity(
        id=uuid4(),
        long_url="https://different.com",
        short_url=short_url,
    )

    assert entity1 == entity2
    assert entity1.short_url == entity2.short_url
    assert entity1.id != entity2.id


def test_url_entity_timestamps():
    entity = URLEntity(
        long_url="https://example.com",
        short_url="abc123",
    )

    assert isinstance(entity.created_at, datetime)
    assert isinstance(entity.updated_at, datetime)
    assert entity.created_at.date() == datetime.today().date()
    assert entity.updated_at.date() == datetime.today().date()
