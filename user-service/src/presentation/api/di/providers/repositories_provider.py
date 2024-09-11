from dishka import Provider, provide, Scope

from sqlalchemy.ext.asyncio import AsyncSession
import redis.asyncio as redis

from src.infra.database.repositories.user import UserRepo, BaseUserRepo
from src.infra.redis.repositories.base import BaseRedisRepository
from src.infra.redis.repositories.user import RedisRepository


class RepositoriesProvider(Provider):
    @provide(scope=Scope.REQUEST)
    def get_user_repo(self, session: AsyncSession) -> BaseUserRepo:
        return UserRepo(_session=session)

    @provide(scope=Scope.REQUEST)
    def get_redis_repo(self, redis_connection: redis.Redis) -> BaseRedisRepository:
        return RedisRepository(redis_connection)
