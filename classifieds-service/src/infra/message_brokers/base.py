from abc import ABC, abstractmethod
from typing import AsyncIterator


class BaseMessageBroker(ABC):
    @abstractmethod
    async def send_message(self, key: bytes, topic: str, value: bytes):
        pass

    @abstractmethod
    async def start_consuming(self, topic: str) -> AsyncIterator[dict]:
        yield {}

    @abstractmethod
    async def stop_consuming(self):
        pass

    @abstractmethod
    async def close(self):
        pass

    @abstractmethod
    async def start(self):
        pass
