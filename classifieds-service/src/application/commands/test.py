from dataclasses import dataclass

from src.application.commands.base import BaseCommand, CommandHandler
from src.domain.entities.test import Test


@dataclass(frozen=True)
class TestCommand(BaseCommand):
    test_id: str
    test_name: str
    test_description: str


@dataclass(frozen=True)
class TestCommandHandler(CommandHandler[TestCommand, None]):
    async def handle(self, command: TestCommand) -> None:
        test = Test(command.test_id, command.test_name, command.test_description)
        test.test_event_call()
        await self._mediator.publish(test.pull_events())
