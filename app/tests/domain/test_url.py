from datetime import datetime
from uuid import uuid4

import pytest

from domain.entities.url import URLEntity
from domain.exceptions.url import (
    EmptyURLError,
    InvalidURLError,
    URLTooLongError,
)
from domain.value_objects.url import (
    LongURLValueObject,
    MAX_URL_LENGTH,
)


@pytest.mark.parametrize(
    "long_url,short_url",
    [
        ("https://example.com", "abc123"),
        ("https://google.com", "xyz789"),
        ("http://example.com/path", "def456"),
        ("https://example.com", ""),
    ],
)
def test_create_url_entity(long_url, short_url):
    entity = URLEntity(
        long_url=LongURLValueObject(value=long_url),
        short_url=short_url,
    )
    assert entity.long_url.value == long_url
    assert entity.short_url == short_url
    assert entity.id is not None
    assert entity.created_at.date() == datetime.today().date()
    assert entity.updated_at.date() == datetime.today().date()


def test_create_url_entity_with_custom_id():
    entity_id = uuid4()
    entity = URLEntity(
        id=entity_id,
        long_url=LongURLValueObject(value="https://example.com"),
        short_url="abc123",
    )

    assert entity.id == entity_id
    assert entity.long_url.value == "https://example.com"
    assert entity.short_url == "abc123"


def test_url_entity_equality_by_short_url():
    entity1 = URLEntity(
        long_url=LongURLValueObject(value="https://example.com"),
        short_url="abc123",
    )

    entity2 = URLEntity(
        long_url=LongURLValueObject(value="https://different.com"),
        short_url="abc123",
    )

    assert entity1 == entity2
    assert hash(entity1) == hash(entity2)


def test_url_entity_inequality_by_different_short_url():
    entity1 = URLEntity(
        long_url=LongURLValueObject(value="https://example.com"),
        short_url="abc123",
    )

    entity2 = URLEntity(
        long_url=LongURLValueObject(value="https://example.com"),
        short_url="xyz789",
    )

    assert entity1 != entity2
    assert hash(entity1) != hash(entity2)


def test_url_entity_uniqueness_by_short_url():
    short_url = "unique123"

    entity1 = URLEntity(
        id=uuid4(),
        long_url=LongURLValueObject(value="https://example.com"),
        short_url=short_url,
    )

    entity2 = URLEntity(
        id=uuid4(),
        long_url=LongURLValueObject(value="https://different.com"),
        short_url=short_url,
    )

    assert entity1 == entity2
    assert entity1.short_url == entity2.short_url
    assert entity1.id != entity2.id


def test_url_entity_timestamps():
    entity = URLEntity(
        long_url=LongURLValueObject(value="https://example.com"),
        short_url="abc123",
    )

    assert isinstance(entity.created_at, datetime)
    assert isinstance(entity.updated_at, datetime)
    assert entity.created_at.date() == datetime.today().date()
    assert entity.updated_at.date() == datetime.today().date()


# Tests for LongURLValueObject validation
def test_long_url_value_object_valid_urls():
    """Test that valid URLs are accepted."""
    valid_urls = [
        "https://example.com",
        "http://example.com",
        "https://example.com/path",
        "http://example.com/path/to/resource",
        "https://subdomain.example.com",
        "https://example.com:8080/path",
        "https://example.com?query=param",
        "https://example.com#fragment",
    ]

    for url in valid_urls:
        value_object = LongURLValueObject(value=url)
        assert value_object.value == url
        assert value_object.as_generic_type() == url


def test_long_url_value_object_empty_url():
    """Test that empty URLs raise EmptyURLError."""
    with pytest.raises(EmptyURLError):
        LongURLValueObject(value="")

    with pytest.raises(EmptyURLError):
        LongURLValueObject(value="   ")


def test_long_url_value_object_url_without_scheme():
    """Test that URLs without scheme raise InvalidURLError."""
    with pytest.raises(InvalidURLError) as exc_info:
        LongURLValueObject(value="example.com")

    assert "scheme" in exc_info.value.message.lower()


def test_long_url_value_object_unsupported_scheme():
    """Test that unsupported schemes raise InvalidURLError."""
    unsupported_schemes = ["ftp", "file", "mailto", "tel"]

    for scheme in unsupported_schemes:
        with pytest.raises(InvalidURLError) as exc_info:
            LongURLValueObject(value=f"{scheme}://example.com")

        assert (
            "unsupported scheme" in exc_info.value.message.lower()
            or "only http and https" in exc_info.value.message.lower()
        )


def test_long_url_value_object_url_too_long():
    """Test that URLs exceeding max length raise URLTooLongError."""
    long_url = "https://example.com/" + "a" * (MAX_URL_LENGTH + 1)

    with pytest.raises(URLTooLongError) as exc_info:
        LongURLValueObject(value=long_url)

    assert exc_info.value.url_length == len(long_url)
    assert exc_info.value.max_length == MAX_URL_LENGTH


def test_long_url_value_object_invalid_url_format():
    """Test that invalid URL formats raise InvalidURLError."""
    invalid_urls = [
        "http://",
        "https://",
        "http://  ",
    ]

    for url in invalid_urls:
        with pytest.raises(InvalidURLError):
            LongURLValueObject(value=url)


def test_long_url_value_object_invalid_domain():
    """Test that URLs with invalid domain format raise InvalidURLError."""
    invalid_domains = [
        "https://abobus",
        "https://invalid",
        "http://nodot",
        "https://123",
    ]

    for url in invalid_domains:
        with pytest.raises(InvalidURLError) as exc_info:
            LongURLValueObject(value=url)
        assert (
            "domain" in exc_info.value.message.lower()
            or "hostname" in exc_info.value.message.lower()
        )


def test_long_url_value_object_valid_domains():
    """Test that URLs with valid domains are accepted."""
    valid_urls = [
        "https://example.com",
        "http://subdomain.example.com",
        "https://localhost",
        "http://127.0.0.1",
        "https://192.168.1.1",
        "http://example.com:8080",
    ]

    for url in valid_urls:
        value_object = LongURLValueObject(value=url)
        assert value_object.value == url
