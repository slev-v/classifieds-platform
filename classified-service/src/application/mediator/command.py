from abc import (
    ABC,
    abstractmethod,
)
from collections import defaultdict
from collections.abc import Iterable
from dataclasses import (
    dataclass,
    field,
)
from typing import Generic

from src.application.commands.base import (
    BaseCommand,
    CommandHandler,
    CR,
    CT,
)


@dataclass(eq=False)
class CommandMediator(ABC, Generic[CT, CR]):
    commands_map: defaultdict[CT, list[CommandHandler]] = field(
        default_factory=lambda: defaultdict(list),
        kw_only=True,
    )

    @abstractmethod
    def register_command(
        self, command: CT, command_handlers: Iterable[CommandHandler[CT, CR]]
    ): ...

    @abstractmethod
    async def handle_command(self, command: BaseCommand) -> Iterable[CR]: ...
