from dishka import provide, Provider, Scope

from src.infra.database.repositories.user import BaseUserRepo
from src.infra.message_brokers.base import BaseMessageBroker
from src.application.commands.test import TestCommandHandler, TestCommand
from src.application.mediator.base import Mediator
from src.application.events.test_event import TestEvent, TestEventHandler

from src.application.services.user import BaseHasherPasswordService
from src.application.commands.user import (
    CreateUserCommand,
    CreateUserCommandHandler,
    DeleteUserCommand,
    DeleteUserCommandHandler,
)
from src.application.events.user import (
    NewUserCreatedEventHandler,
    UserDeletedEventHandler,
)
from src.application.queries.user import GetUserByOidQuery, GetUserByOidQueryHandler
from src.domain.events.user import NewUserCreatedEvent, UserDeletedEvent


class ApplicationProvider(Provider):
    @provide(scope=Scope.REQUEST)
    async def init_mediator(
        self,
        message_broker: BaseMessageBroker,
        hasher_password: BaseHasherPasswordService,
        user_repo: BaseUserRepo,
    ) -> Mediator:
        mediator = Mediator()

        # command handlers
        create_user_command_handler = CreateUserCommandHandler(
            _mediator=mediator, hasher_password=hasher_password, user_repo=user_repo
        )
        delete_user_command_handler = DeleteUserCommandHandler(
            _mediator=mediator, user_repo=user_repo
        )
        test_command_handler = TestCommandHandler(_mediator=mediator)

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

        test_event_handler = TestEventHandler(
            broker_topic="test-topic",
            message_broker=message_broker,
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
            TestEvent,
            [test_event_handler],
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
            TestCommand,
            [test_command_handler],
        )

        # Queries
        mediator.register_query(
            GetUserByOidQuery,
            get_user_by_oid_query_handler,
        )

        return mediator
