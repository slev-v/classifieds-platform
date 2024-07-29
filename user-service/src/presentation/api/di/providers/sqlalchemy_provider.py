from dishka import provide, Provider, Scope

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
from typing import AsyncGenerator

from src.presentation.api.config import WebConfig
from src.infra.database.connection import create_session_maker, new_session


class SQLAlchemyProvider(Provider):
    @provide(scope=Scope.APP)
    def create_session_maker(self, config: WebConfig) -> async_sessionmaker:
        return create_session_maker(config)

    @provide(scope=Scope.REQUEST)
    async def new_session(
        self, session_maker: async_sessionmaker
    ) -> AsyncGenerator[AsyncSession, None]:
        async for session in new_session(session_maker):
            yield session
