from dishka import provide, Provider, Scope

from src.infra.message_brokers.base import BaseMessageBroker
from src.application.commands.test import TestCommandHandler, TestCommand
from src.application.mediator.base import Mediator
from src.application.events.test_event import TestEvent, TestEventHandler

from src.application.commands.user import CreateUserCommand, CreateUserCommandHandler
from src.application.events.user import NewUserCreatedEventHandler
from src.domain.events.user import NewUserCreatedEvent


class ApplicationProvider(Provider):
    @provide(scope=Scope.APP)
    async def init_mediator(self, message_broker: BaseMessageBroker) -> Mediator:
        mediator = Mediator()

        # command handlers
        create_user_command_handler = CreateUserCommandHandler(_mediator=mediator)
        test_command_handler = TestCommandHandler(_mediator=mediator)

        # event handlers
        new_user_created_event_handler = NewUserCreatedEventHandler(
            broker_topic="new-user-created",
            message_broker=message_broker,
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
            TestEvent,
            [test_event_handler],
        )

        # commands
        mediator.register_command(
            CreateUserCommand,
            [create_user_command_handler],
        )

        mediator.register_command(
            TestCommand,
            [test_command_handler],
        )

        # Queries

        return mediator
