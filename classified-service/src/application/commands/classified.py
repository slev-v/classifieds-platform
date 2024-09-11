from dataclasses import dataclass

from src.domain.entities.classified import Classified
from src.application.commands.base import BaseCommand, CommandHandler
from src.infra.database.repositories.classified import BaseClassifiedRepo


@dataclass(frozen=True)
class CreateClassifiedCommand(BaseCommand):
    title: str
    description: str
    price: float
    owner_oid: str


@dataclass(frozen=True)
class CreateClassifiedCommandHandler(
    CommandHandler[CreateClassifiedCommand, Classified]
):
    classified_repo: BaseClassifiedRepo

    async def handle(self, command: CreateClassifiedCommand) -> Classified:
        new_classified = Classified.create_classified(
            title=command.title,
            description=command.description,
            price=command.price,
            owner_oid=command.owner_oid,
        )

        await self.classified_repo.create_new_classified(new_classified)
        await self._mediator.publish(new_classified.pull_events())

        return new_classified
