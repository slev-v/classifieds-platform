from functools import lru_cache

from dishka import AsyncContainer, make_async_container
from dishka.integrations.faststream import FastStreamProvider

from src.presentation.api.di.providers.application_provider import ApplicationProvider
from src.presentation.api.di.providers.config_provider import ConfigProvider
from src.presentation.api.di.providers.broker_provider import BrokerProvider
from src.presentation.api.di.providers.services_provider import ServicesProvider
from src.presentation.api.di.providers.sqlalchemy_provider import SQLAlchemyProvider
from src.presentation.api.di.providers.repositories_provider import RepositoriesProvider
from src.presentation.api.di.providers.redis_provider import RedisProvider


@lru_cache(1)
def init_container() -> AsyncContainer:
    return _init_container()


def _init_container() -> AsyncContainer:
    container = make_async_container(
        ApplicationProvider(),
        BrokerProvider(),
        ConfigProvider(),
        ServicesProvider(),
        SQLAlchemyProvider(),
        RepositoriesProvider(),
        RedisProvider(),
    )
    return container
