from dataclasses import dataclass

from src.application.services.base import BaseSessionService
from src.domain.entities.user import User, Session
from src.domain.values.user import Email, RawPassword, Username
from src.application.commands.base import BaseCommand, CommandHandler
from src.application.services.user import BaseHasherPasswordService
from src.application.exceptions.user import (
    PasswordNotMatchException,
    UserNotFoundException,
    UserNotFoundByNameException,
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
    session_oid: str


@dataclass(frozen=True)
class DeleteUserCommandHandler(CommandHandler[DeleteUserCommand, None]):
    user_repo: BaseUserRepo
    session_service: BaseSessionService

    async def handle(self, command: DeleteUserCommand) -> None:
        user_oid = await self.session_service.get(command.session_oid)
        user = await self.user_repo.get_user_by_oid(oid=user_oid)

        if not user:
            raise UserNotFoundException(user_oid=user_oid)

        await self.user_repo.delete_user_by_oid(user_oid)
        await self.session_service.delete_session(command.session_oid)
        user.delete()
        await self._mediator.publish(user.pull_events())


@dataclass(frozen=True)
class LogoutUserCommand(BaseCommand):
    session_oid: str


@dataclass(frozen=True)
class LogoutUserCommandHandler(CommandHandler[LogoutUserCommand, None]):
    session_service: BaseSessionService
    user_repo: BaseUserRepo

    async def handle(self, command: LogoutUserCommand) -> None:
        user_oid = await self.session_service.get(command.session_oid)
        user = await self.user_repo.get_user_by_oid(user_oid)

        if not user:
            raise UserNotFoundException(user_oid=user_oid)

        user.logout(command.session_oid)
        await self.session_service.delete_session(command.session_oid)
        await self._mediator.publish(user.pull_events())


@dataclass(frozen=True)
class LoginUserCommand(BaseCommand):
    username: str
    password: str


@dataclass(frozen=True)
class LoginUserCommandHandler(CommandHandler[LoginUserCommand, str]):
    hasher_password: BaseHasherPasswordService
    session_service: BaseSessionService
    user_repo: BaseUserRepo

    async def handle(self, command: LoginUserCommand) -> str:
        user = await self.user_repo.get_user_by_username(command.username)

        if not user:
            raise UserNotFoundByNameException(command.username)

        if not self.hasher_password.verify_password(
            command.password, user.hashed_password
        ):
            raise PasswordNotMatchException()

        session = Session(user_oid=user.oid)
        user.login(session.oid)

        await self.session_service.create_session(
            session_oid=session.oid, user_oid=user.oid
        )
        await self._mediator.publish(user.pull_events())

        return session.oid
