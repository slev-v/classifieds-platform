from functools import lru_cache

from dishka import AsyncContainer, make_async_container

from src.presentation.api.di.providers.application_provider import ApplicationProvider
from src.presentation.api.di.providers.config_provider import ConfigProvider
from src.presentation.api.di.providers.kafka_provider import KafkaProvider
from src.presentation.api.di.providers.services_provider import ServicesProvider
from src.presentation.api.di.providers.sqlalchemy_provider import SQLAlchemyProvider
from src.presentation.api.di.providers.repositories_provider import RepositoriesProvider
from src.presentation.api.di.providers.redis_provider import RedisProvider


@lru_cache(1)
def init_container() -> AsyncContainer:
    return make_async_container(
        KafkaProvider(),
        ConfigProvider(),
        ApplicationProvider(),
        ServicesProvider(),
        SQLAlchemyProvider(),
        RepositoriesProvider(),
        RedisProvider(),
    )
