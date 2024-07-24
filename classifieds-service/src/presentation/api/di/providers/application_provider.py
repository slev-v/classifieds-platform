from dishka import provide, Provider, Scope

from src.infra.message_brokers.base import BaseMessageBroker
from src.application.commands.test import TestCommandHandler, TestCommand
from src.application.mediator.base import Mediator
from src.application.events.test_event import TestEvent, TestEventHandler


class ApplicationProvider(Provider):
    @provide(scope=Scope.APP)
    async def init_mediator(self, message_broker: BaseMessageBroker) -> Mediator:
        mediator = Mediator()

        # command handlers
        test_command_handler = TestCommandHandler(_mediator=mediator)

        # event handlers
        test_event_handler = TestEventHandler(
            broker_topic="test-topic",
            message_broker=message_broker,
        )

        # events
        mediator.register_event(
            TestEvent,
            [test_event_handler],
        )

        # commands
        mediator.register_command(
            TestCommand,
            [test_command_handler],
        )

        # Queries

        return mediator
