from dataclasses import dataclass

from src.domain.entities.user import User
from src.domain.values.user import Email, RawPassword, Username
from src.application.commands.base import BaseCommand, CommandHandler
from src.application.services.user import BaseHasherPasswordService
from src.application.exceptions.user import (
    UserNotFoundException,
    EmailAlreadyExistsException,
    UsernameAlreadyExistsException,
)
from src.infra.database.repositories.user import BaseUserRepo


@dataclass(frozen=True)
class CreateUserCommand(BaseCommand):
    name: str
    email: str
    password: str


@dataclass(frozen=True)
class CreateUserCommandHandler(CommandHandler[CreateUserCommand, User]):
    hasher_password: BaseHasherPasswordService
    user_repo: BaseUserRepo

    async def handle(self, command: CreateUserCommand) -> User:
        user_exist = await self.user_repo.check_user_exist_by_email_or_username(
            command.email, command.name
        )

        # NOTE: May be better to use a sepparate functions for email and username
        if user_exist and user_exist.email.as_generic_type() == command.email:
            raise EmailAlreadyExistsException(email=command.email)
        elif user_exist and user_exist.name.as_generic_type() == command.name:
            raise UsernameAlreadyExistsException(username=command.name)

        name = Username(value=command.name)
        email = Email(value=command.email)
        raw_password = RawPassword(value=command.password)

        hashed_password = self.hasher_password.get_password_hash(
            raw_password.as_generic_type()
        )

        new_user = User.create_user(
            name=name, email=email, hashed_password=hashed_password
        )

        await self.user_repo.create_new_user(new_user)
        await self._mediator.publish(new_user.pull_events())

        return new_user


@dataclass(frozen=True)
class DeleteUserCommand(BaseCommand):
    user_oid: str


@dataclass(frozen=True)
class DeleteUserCommandHandler(CommandHandler[DeleteUserCommand, None]):
    user_repo: BaseUserRepo

    async def handle(self, command: DeleteUserCommand) -> None:
        user = await self.user_repo.get_user_by_oid(oid=command.user_oid)

        if not user:
            raise UserNotFoundException(user_oid=command.user_oid)

        await self.user_repo.delete_user_by_oid(command.user_oid)
        user.delete()
        await self._mediator.publish(user.pull_events())


# @dataclass(frozen=True)
# class DeleteChatCommand(BaseCommand):
#     chat_oid: str
#
#
# @dataclass(frozen=True)
# class DeleteChatCommandHandler(CommandHandler[DeleteChatCommand, None]):
#     chats_repository: BaseChatsRepository
#
#     async def handle(self, command: DeleteChatCommand) -> None:
#         chat = await self.chats_repository.get_chat_by_oid(oid=command.chat_oid)
#
#         if not chat:
#             raise ChatNotFoundException(chat_oid=command.chat_oid)
#
#         await self.chats_repository.delete_chat_by_oid(chat_oid=command.chat_oid)
#         chat.delete()
#         await self._mediator.publish(chat.pull_events())
