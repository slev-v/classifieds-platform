from dataclasses import dataclass
from typing import ClassVar

from src.domain.events.user import NewUserCreatedEvent
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
