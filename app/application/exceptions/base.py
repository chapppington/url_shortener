from dataclasses import dataclass

from domain.exceptions.base import DomainException


@dataclass(eq=False)
class ApplicationException(DomainException):
    @property
    def message(self) -> str:
        return "Application exception occurred"
