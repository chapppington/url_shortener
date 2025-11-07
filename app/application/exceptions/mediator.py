from dataclasses import dataclass

from application.exceptions.base import ApplicationException


@dataclass(eq=False)
class CommandHandlersNotRegisteredException(ApplicationException):
    command_type: type

    @property
    def message(self) -> str:
        return f"Command handlers not registered for command type: {self.command_type.__name__}"


@dataclass(eq=False)
class QueryHandlerNotRegisteredException(ApplicationException):
    query_type: type

    @property
    def message(self) -> str:
        return (
            f"Query handler not registered for query type: {self.query_type.__name__}"
        )
