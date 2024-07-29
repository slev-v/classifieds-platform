from uuid import uuid4

from dishka import provide, Provider, Scope
from aiokafka import AIOKafkaConsumer, AIOKafkaProducer

from src.infra.message_brokers.base import BaseMessageBroker
from src.infra.message_brokers.kafka import KafkaMessageBroker
from src.presentation.api.config import WebConfig


class KafkaProvider(Provider):
    @provide(scope=Scope.APP)
    def create_message_broker(self, config: WebConfig) -> BaseMessageBroker:
        return KafkaMessageBroker(
            producer=AIOKafkaProducer(bootstrap_servers=config.kafka_uri),
            consumer=AIOKafkaConsumer(
                bootstrap_servers=config.kafka_uri,
                group_id=str(uuid4()),
                metadata_max_age_ms=30000,
            ),
        )
