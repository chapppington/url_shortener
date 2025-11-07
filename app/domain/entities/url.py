from dataclasses import dataclass

from domain.entities.base import BaseEntity


@dataclass
class URLEntity(BaseEntity):
    short_url: str
    long_url: str

    def __hash__(self) -> int:
        return hash(self.short_url)

    def __eq__(self, other: "URLEntity") -> bool:
        return self.short_url == other.short_url
