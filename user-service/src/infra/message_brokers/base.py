from abc import ABC, abstractmethod


class BaseMessageBroker(ABC):
    @abstractmethod
    async def send_message(self, key: bytes, topic: str, value: bytes):
        pass

    @abstractmethod
    async def start(self):
        pass

    @abstractmethod
    async def stop(self) -> None:
        pass
