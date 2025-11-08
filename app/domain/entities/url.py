from dataclasses import dataclass

from domain.entities.base import BaseEntity
from domain.value_objects.url import LongURLValueObject


@dataclass
class URLEntity(BaseEntity):
    short_url: str
    long_url: LongURLValueObject

    def __hash__(self) -> int:
        return hash(self.short_url)

    def __eq__(self, other: "URLEntity") -> bool:
        return self.short_url == other.short_url
