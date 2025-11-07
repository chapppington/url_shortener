from dataclasses import dataclass


@dataclass(eq=False)
class DomainException(Exception):
    @property
    def message(self) -> str:
        return "Domain exception occurred"
