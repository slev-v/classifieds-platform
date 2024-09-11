from dataclasses import dataclass

from src.application.events.base import EventHandler
from src.domain.events.classified import NewClassifiedCreatedEvent
from src.infra.message_brokers.converters import convert_event_to_broker_message


@dataclass
class NewClassifiedCreatedEventHandler(EventHandler[NewClassifiedCreatedEvent, None]):
    async def handle(self, event: NewClassifiedCreatedEvent) -> None:
        await self.message_broker.send_message(
            topic=self.broker_topic,
            value=convert_event_to_broker_message(event=event),
            key=str(event.event_id).encode(),
        )
