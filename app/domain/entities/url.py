from dataclasses import dataclass

from domain.entities.base import BaseEntity


@dataclass
class URLEntity(BaseEntity):
    shortURL: str
    longURL: str
