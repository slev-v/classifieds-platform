from dishka import provide, Provider, Scope

import redis.asyncio as redis

from src.presentation.api.config import WebConfig
from src.infra.redis.connection import create_redis_pool, new_redis_connection


class RedisProvider(Provider):
    @provide(scope=Scope.APP)
    def create_redis_pool(self, config: WebConfig) -> redis.ConnectionPool:
        return create_redis_pool(config)

    @provide(scope=Scope.REQUEST)
    def new_redis_connection(self, redis_pool: redis.ConnectionPool) -> redis.Redis:
        return new_redis_connection(redis_pool)
