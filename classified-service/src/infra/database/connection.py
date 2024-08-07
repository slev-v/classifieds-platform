from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from typing import AsyncContextManager, AsyncGenerator, Callable

from src.presentation.api.config import WebConfig


def create_session_maker(config: WebConfig) -> async_sessionmaker:
    db_uri = config.async_db_uri

    engine = create_async_engine(db_uri, pool_size=15, max_overflow=15)
    return async_sessionmaker(engine, autoflush=False, expire_on_commit=False)


async def new_session(
    session_maker: Callable[[], AsyncContextManager],
) -> AsyncGenerator:
    async with session_maker() as session:
        yield session
