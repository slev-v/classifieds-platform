from dishka import provide, Provider, Scope

from src.application.services.base import BaseHasherPasswordService, BaseSessionService
from src.application.services.user import HasherPasswordService, SessionService
from src.infra.redis.repositories.base import BaseRedisRepository
from src.presentation.api.config import WebConfig


class ServicesProvider(Provider):
    @provide(scope=Scope.APP)
    async def get_hasher_password(self) -> BaseHasherPasswordService:
        return HasherPasswordService()

    @provide(scope=Scope.REQUEST)
    async def get_session_service(
        self, config: WebConfig, redis_repo: BaseRedisRepository
    ) -> BaseSessionService:
        return SessionService(config, redis_repo)
