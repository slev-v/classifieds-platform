from dataclasses import dataclass
from abc import ABC, abstractmethod


@dataclass
class BaseRedisRepository(ABC):
    @abstractmethod
    async def get(self, key: str) -> bytes | None: ...

    @abstractmethod
    async def set_with_ex(self, key: str, value: str, ex: int) -> None: ...

    @abstractmethod
    async def delete(self, key: str) -> None: ...

    @abstractmethod
    async def exists(self, key: str) -> bool: ...
