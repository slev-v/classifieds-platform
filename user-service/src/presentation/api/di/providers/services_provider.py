from dishka import provide, Provider, Scope

from src.application.services.base import BaseHasherPasswordService
from src.application.services.user import HasherPasswordService


class ServicesProvider(Provider):
    @provide(scope=Scope.APP)
    async def get_hasher_password(self) -> BaseHasherPasswordService:
        return HasherPasswordService()
