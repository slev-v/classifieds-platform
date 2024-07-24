from dataclasses import dataclass

from src.domain.entities.user import User
from src.domain.values.user import Email, Username
from src.application.commands.base import BaseCommand, CommandHandler


@dataclass(frozen=True)
class CreateUserCommand(BaseCommand):
    name: str
    email: str


@dataclass(frozen=True)
class CreateUserCommandHandler(CommandHandler[CreateUserCommand, User]):
    async def handle(self, command: CreateUserCommand) -> User:
        name = Username(value=command.name)
        email = Email(value=command.email)
        new_user = User.create_user(name=name, email=email, hashed_password="123")

        await self._mediator.publish(new_user.pull_events())

        return new_user
