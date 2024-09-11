from dataclasses import dataclass

from src.domain.events.user import (
    NewUserCreatedEvent,
    UserDeletedEvent,
    UserLoggedInEvent,
    UserLoggedOutEvent,
)
from src.application.events.base import EventHandler
from src.infra.message_brokers.converters import convert_event_to_broker_message


@dataclass
class NewUserCreatedEventHandler(EventHandler[NewUserCreatedEvent, None]):
    async def handle(self, event: NewUserCreatedEvent) -> None:
        await self.message_broker.send_message(
            topic=self.broker_topic,
            value=convert_event_to_broker_message(event=event),
            key=str(event.event_id).encode(),
        )


@dataclass
class UserDeletedEventHandler(EventHandler[UserDeletedEvent, None]):
    async def handle(self, event: UserDeletedEvent) -> None:
        await self.message_broker.send_message(
            topic=self.broker_topic,
            value=convert_event_to_broker_message(event=event),
            key=str(event.event_id).encode(),
        )


@dataclass
class UserLoggedInEventHandler(EventHandler[UserLoggedInEvent, None]):
    async def handle(self, event: UserLoggedInEvent) -> None:
        await self.message_broker.send_message(
            topic=self.broker_topic,
            value=convert_event_to_broker_message(event=event),
            key=str(event.event_id).encode(),
        )


@dataclass
class UserLoggedOutEventHandler(EventHandler[UserLoggedOutEvent, None]):
    async def handle(self, event: UserLoggedOutEvent) -> None:
        await self.message_broker.send_message(
            topic=self.broker_topic,
            value=convert_event_to_broker_message(event=event),
            key=str(event.event_id).encode(),
        )
