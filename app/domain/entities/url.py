from dataclasses import dataclass

from domain.entities.base import BaseEntity


@dataclass
class URLEntity(BaseEntity):
    short_url: str
    long_url: str
