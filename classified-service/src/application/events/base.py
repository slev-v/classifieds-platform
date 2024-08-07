from abc import (
    ABC,
    abstractmethod,
)
from dataclasses import dataclass
from typing import (
    Any,
    Generic,
    TypeVar,
    Coroutine,
)

from src.domain.events.base import BaseEvent
from src.infra.message_brokers.base import BaseMessageBroker

# from infra.websockets.managers import BaseConnectionManager


ET = TypeVar("ET", bound=BaseEvent)
ER = TypeVar("ER", bound=Any)


@dataclass
class IntegrationEvent(BaseEvent, ABC): ...


@dataclass
class EventHandler(ABC, Generic[ET, ER]):
    message_broker: BaseMessageBroker
    # connection_manager: BaseConnectionManager
    broker_topic: str

    @abstractmethod
    def handle(self, event: ET) -> Coroutine[Any, Any, ER]: ...
