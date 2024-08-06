import redis.asyncio as redis

from src.presentation.api.config import WebConfig


def create_redis_pool(config: WebConfig) -> redis.ConnectionPool:
    return redis.ConnectionPool.from_url(config.redis_uri)


def new_redis_connection(redis_pool) -> redis.Redis:
    return redis.Redis(connection_pool=redis_pool)
