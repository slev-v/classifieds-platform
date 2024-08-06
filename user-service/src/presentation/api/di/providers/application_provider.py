from dishka import provide, Provider, Scope

from src.application.services.base import BaseSessionService
from src.infra.database.repositories.user import BaseUserRepo
from src.infra.message_brokers.base import BaseMessageBroker
from src.application.mediator.base import Mediator

from src.application.services.user import BaseHasherPasswordService
from src.application.commands.user import (
    CreateUserCommand,
    CreateUserCommandHandler,
    DeleteUserCommand,
    DeleteUserCommandHandler,
    LoginUserCommand,
    LoginUserCommandHandler,
    LogoutUserCommand,
    LogoutUserCommandHandler,
)
from src.application.events.user import (
    NewUserCreatedEventHandler,
    UserDeletedEventHandler,
    UserLoggedInEventHandler,
    UserLoggedOutEventHandler,
)
from src.application.queries.user import GetUserByOidQuery, GetUserByOidQueryHandler
from src.domain.events.user import (
    NewUserCreatedEvent,
    UserDeletedEvent,
    UserLoggedInEvent,
    UserLoggedOutEvent,
)


class ApplicationProvider(Provider):
    @provide(scope=Scope.REQUEST)
    async def init_mediator(
        self,
        message_broker: BaseMessageBroker,
        hasher_password: BaseHasherPasswordService,
        session_service: BaseSessionService,
        user_repo: BaseUserRepo,
    ) -> Mediator:
        mediator: Mediator = Mediator()

        # command handlers
        create_user_command_handler = CreateUserCommandHandler(
            _mediator=mediator, hasher_password=hasher_password, user_repo=user_repo
        )
        delete_user_command_handler = DeleteUserCommandHandler(
            _mediator=mediator, user_repo=user_repo, session_service=session_service
        )
        login_user_command_handler = LoginUserCommandHandler(
            _mediator=mediator,
            user_repo=user_repo,
            hasher_password=hasher_password,
            session_service=session_service,
        )
        logout_user_command_handler = LogoutUserCommandHandler(
            _mediator=mediator, session_service=session_service, user_repo=user_repo
        )

        # query handlers
        get_user_by_oid_query_handler = GetUserByOidQueryHandler(user_repo=user_repo)

        # event handlers
        new_user_created_event_handler = NewUserCreatedEventHandler(
            broker_topic="new-user-created",
            message_broker=message_broker,
        )

        user_deleted_event_handler = UserDeletedEventHandler(
            broker_topic="user-deleted", message_broker=message_broker
        )

        user_logged_in_event_handler = UserLoggedInEventHandler(
            broker_topic="user-logged-in", message_broker=message_broker
        )

        user_logged_out_event_handler = UserLoggedOutEventHandler(
            broker_topic="user-logged-out", message_broker=message_broker
        )

        # events
        mediator.register_event(
            NewUserCreatedEvent,
            [new_user_created_event_handler],
        )

        mediator.register_event(
            UserDeletedEvent,
            [user_deleted_event_handler],
        )

        mediator.register_event(
            UserLoggedInEvent,
            [user_logged_in_event_handler],
        )

        mediator.register_event(
            UserLoggedOutEvent,
            [user_logged_out_event_handler],
        )

        # commands
        mediator.register_command(
            CreateUserCommand,
            [create_user_command_handler],
        )

        mediator.register_command(
            DeleteUserCommand,
            [delete_user_command_handler],
        )

        mediator.register_command(
            LoginUserCommand,
            [login_user_command_handler],
        )

        mediator.register_command(
            LogoutUserCommand,
            [logout_user_command_handler],
        )

        # Queries
        mediator.register_query(
            GetUserByOidQuery,
            get_user_by_oid_query_handler,
        )

        return mediator
