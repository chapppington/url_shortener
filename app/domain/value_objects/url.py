import re
from dataclasses import dataclass
from ipaddress import (
    AddressValueError,
    ip_address,
)
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
        netloc = parsed.netloc.strip() if parsed.netloc else ""
        if not netloc:
            raise InvalidURLError(
                url=self.value,
                reason="URL must include a domain (e.g., example.com)",
            )

        # Validate domain format
        # Remove port if present (e.g., example.com:8080 -> example.com)
        domain = netloc.split(":")[0]

        # Check if it's localhost (allowed)
        is_localhost = domain.lower() in ("localhost", "127.0.0.1", "::1")

        # Check if it's a valid IP address (allowed)
        is_ip = False
        try:
            ip_address(domain)
            is_ip = True
        except (ValueError, AddressValueError):
            pass

        # Check if it's a valid domain name (must contain at least one dot for TLD)
        # Domain pattern: alphanumeric, hyphens, dots, must have at least one dot
        is_valid_domain = bool(
            re.match(
                r"^([a-zA-Z0-9]([a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?\.)+[a-zA-Z]{2,}$",
                domain,
            ),
        )

        if not (is_localhost or is_ip or is_valid_domain):
            raise InvalidURLError(
                url=self.value,
                reason=f"Invalid domain format '{domain}'. Domain must be a valid hostname (e.g., example.com), IP address, or localhost",
            )

        # Scheme must be http or https
        if parsed.scheme not in ("http", "https"):
            raise InvalidURLError(
                url=self.value,
                reason=f"Unsupported scheme '{parsed.scheme}'. Only http and https are allowed",
            )

    def as_generic_type(self) -> str:
        return str(self.value)
