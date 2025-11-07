from dataclasses import dataclass

from domain.exceptions.base import DomainException


@dataclass(eq=False)
class LongURLNotFoundException(DomainException):
    short_url: str

    @property
    def message(self) -> str:
        return f"Long URL not found for short URL: {self.short_url}"
