import os
from dotenv import load_dotenv
from dataclasses import dataclass

DB_URI_ENV = "DB_URI"
REDIS_URI_ENV = "REDIS_URI"
KAFKA_URI_ENV = "KAFKA_URI"
SESSION_EXPIRE_TIME_ENV = "SESSION_EXPIRE_TIME"


class ConfigParseError(ValueError):
    pass


@dataclass
class WebConfig:
    async_db_uri: str
    db_uri: str
    redis_uri: str
    kafka_uri: str
    session_expire_time: int


def get_str_env(key: str) -> str:
    val = os.getenv(key)
    if not val:
        raise ConfigParseError(f"{key} is not set")
    return val


def load_web_config() -> WebConfig:
    load_dotenv()
    async_db_uri = f"postgresql+asyncpg://{get_str_env(DB_URI_ENV)}"
    db_uri = f"postgresql://{get_str_env(DB_URI_ENV)}"
    redis_uri = get_str_env(REDIS_URI_ENV)
    kafka_uri = get_str_env(KAFKA_URI_ENV)
    session_expire_time = int(get_str_env(SESSION_EXPIRE_TIME_ENV))
    return WebConfig(
        async_db_uri=async_db_uri,
        db_uri=db_uri,
        redis_uri=redis_uri,
        kafka_uri=kafka_uri,
        session_expire_time=session_expire_time,
    )
