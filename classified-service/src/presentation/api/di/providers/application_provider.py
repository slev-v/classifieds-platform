from dishka import provide, Provider, Scope

from src.domain.events.classified import NewClassifiedCreatedEvent
from src.infra.database.repositories.classified import BaseClassifiedRepo
from src.infra.message_brokers.base import BaseMessageBroker
from src.application.commands.classified import (
    CreateClassifiedCommand,
    CreateClassifiedCommandHandler,
)
from src.application.mediator.base import Mediator
from src.application.events.classified import NewClassifiedCreatedEventHandler


class ApplicationProvider(Provider):
    @provide(scope=Scope.REQUEST)
    async def init_mediator(
        self, classified_repo: BaseClassifiedRepo, message_broker: BaseMessageBroker
    ) -> Mediator:
        mediator = Mediator()

        # command handlers
        create_classified_command_handler = CreateClassifiedCommandHandler(
            _mediator=mediator, classified_repo=classified_repo
        )

        # event handlers
        new_classified_created_event_handler = NewClassifiedCreatedEventHandler(
            broker_topic="classified-created",
            message_broker=message_broker,
        )

        # events
        mediator.register_event(
            NewClassifiedCreatedEvent,
            [new_classified_created_event_handler],
        )

        # commands
        mediator.register_command(
            CreateClassifiedCommand,
            [create_classified_command_handler],
        )

        # Queries

        return mediator
