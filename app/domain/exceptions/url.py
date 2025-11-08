from dataclasses import dataclass

from domain.exceptions.base import DomainException


@dataclass(eq=False)
class LongURLNotFoundException(DomainException):
    short_url: str

    @property
    def message(self) -> str:
        return f"Long URL not found for short URL: {self.short_url}"


@dataclass(eq=False)
class EmptyURLError(DomainException):
    @property
    def message(self) -> str:
        return "URL cannot be empty"


@dataclass(eq=False)
class InvalidURLError(DomainException):
    url: str
    reason: str

    @property
    def message(self) -> str:
        return f"Invalid URL '{self.url}': {self.reason}"


@dataclass(eq=False)
class URLTooLongError(DomainException):
    url_length: int
    max_length: int

    @property
    def message(self) -> str:
        return f"URL is too long: {self.url_length} characters (maximum: {self.max_length})"
