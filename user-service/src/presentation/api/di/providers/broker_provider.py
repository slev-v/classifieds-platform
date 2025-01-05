from dishka import Provider, provide, Scope
from faststream.nats import NatsBroker

from src.infra.message_brokers.base import BaseMessageBroker
from src.infra.message_brokers.faststream_broker import FastStreamMessageBroker
from src.presentation.api.config import WebConfig


class BrokerProvider(Provider):
    @provide(scope=Scope.APP)
    async def get_broker(self, config: WebConfig) -> NatsBroker:
        return NatsBroker(config.nats_uri)

    @provide(scope=Scope.APP)
    async def get_broker_repo(self, broker: NatsBroker) -> BaseMessageBroker:
        return FastStreamMessageBroker(broker)
