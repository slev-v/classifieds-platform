import os
from dataclasses import dataclass

DB_URI_ENV = "DB_URI"
KAFKA_URI_ENV = "KAFKA_URI"


class ConfigParseError(ValueError):
    pass


@dataclass
class WebConfig:
    async_db_uri: str
    db_uri: str
    kafka_uri: str


def get_str_env(key: str) -> str:
    val = os.getenv(key)
    if not val:
        raise ConfigParseError(f"{key} is not set")
    return val


def load_web_config() -> WebConfig:
    async_db_uri = f"postgresql+asyncpg://{get_str_env(DB_URI_ENV)}"
    db_uri = f"postgresql://{get_str_env(DB_URI_ENV)}"
    kafka_uri = get_str_env(KAFKA_URI_ENV)
    return WebConfig(
        async_db_uri=async_db_uri,
        db_uri=db_uri,
        kafka_uri=kafka_uri,
    )
