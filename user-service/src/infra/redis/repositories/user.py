from dataclasses import dataclass

import redis.asyncio as redis

from src.infra.redis.repositories.base import BaseRedisRepository


@dataclass
class RedisRepository(BaseRedisRepository):
    def __init__(self, connection: redis.Redis) -> None:
        self.connection = connection

    async def get(self, key: str) -> bytes | None:
        return await self.connection.get(key)

    async def set_with_ex(self, key: str, value: str, ex: int) -> None:
        await self.connection.set(key, value, ex=ex)

    async def delete(self, key: str) -> None:
        await self.connection.delete(key)

    async def exists(self, key: str) -> bool:
        return await self.connection.exists(key)
