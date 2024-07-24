from dataclasses import dataclass
from typing import ClassVar

from src.infra.message_brokers.converters import convert_event_to_broker_message
from src.application.events.base import IntegrationEvent, EventHandler


@dataclass
class TestEvent(IntegrationEvent):
    event_title: ClassVar[str] = "Test Event"

    test_id: str
    test_name: str
    test_description: str


@dataclass
class TestEventHandler(EventHandler[TestEvent, None]):
    async def handle(self, event: TestEvent) -> None:
        await self.message_broker.send_message(
            topic=self.broker_topic,
            value=convert_event_to_broker_message(event=event),
            key=str(event.test_id).encode(),
        )


# @dataclass
# class NewMessageReceivedEventHandler(EventHandler[NewMessageReceivedEvent, None]):
#     async def handle(self, event: NewMessageReceivedEvent) -> None:
#         await self.message_broker.send_message(
#             topic=self.broker_topic,
#             value=convert_event_to_broker_message(event=event),
#             key=event.chat_oid.encode(),
#         )
