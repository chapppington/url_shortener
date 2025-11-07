from dataclasses import dataclass

from application.commands.base import (
    BaseCommand,
    BaseCommandHandler,
)
from domain.services.url import URLService


@dataclass(frozen=True)
class CreateShortURLCommand(BaseCommand):
    long_url: str


@dataclass(frozen=True)
class CreateShortURLCommandHandler(
    BaseCommandHandler[CreateShortURLCommand, str],
):
    url_service: URLService

    async def handle(self, command: CreateShortURLCommand) -> str:
        short_url = await self.url_service.get_or_create_short_url(
            long_url=command.long_url,
        )
        return short_url
