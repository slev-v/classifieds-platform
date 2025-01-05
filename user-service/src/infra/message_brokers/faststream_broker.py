from dataclasses import dataclass

from faststream.nats.fastapi import NatsBroker

from src.infra.message_brokers.base import BaseMessageBroker


@dataclass
class FastStreamMessageBroker(BaseMessageBroker):
    broker: NatsBroker

    async def send_message(self, key: bytes, topic: str, value: bytes):
        await self.broker.publish(subject=topic, message=value)

    async def start(self):
        await self.broker.connect()

    async def stop(self):
        await self.broker.close()
