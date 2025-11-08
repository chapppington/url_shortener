from dataclasses import dataclass
from urllib.parse import urlparse

from domain.exceptions.url import (
    EmptyURLError,
    InvalidURLError,
    URLTooLongError,
)
from domain.value_objects.base import BaseValueObject


MAX_URL_LENGTH = 2048


@dataclass(frozen=True)
class LongURLValueObject(BaseValueObject[str]):
    value: str

    def validate(self):
        if not self.value or not self.value.strip():
            raise EmptyURLError()

        if len(self.value) > MAX_URL_LENGTH:
            raise URLTooLongError(
                url_length=len(self.value),
                max_length=MAX_URL_LENGTH,
            )

        parsed = urlparse(self.value)

        # URL must have a scheme (http, https, etc.)
        if not parsed.scheme:
            raise InvalidURLError(
                url=self.value,
                reason="URL must include a scheme (e.g., http:// or https://)",
            )

        # URL must have a netloc (domain) - check both empty and whitespace-only
        if not parsed.netloc or not parsed.netloc.strip():
            raise InvalidURLError(
                url=self.value,
                reason="URL must include a domain (e.g., example.com)",
            )

        # Scheme must be http or https
        if parsed.scheme not in ("http", "https"):
            raise InvalidURLError(
                url=self.value,
                reason=f"Unsupported scheme '{parsed.scheme}'. Only http and https are allowed",
            )

    def as_generic_type(self) -> str:
        return str(self.value)
