from dishka import provide, Provider, Scope

from src.presentation.api.config import WebConfig, load_web_config


class ConfigProvider(Provider):
    @provide(scope=Scope.APP)
    def init_config(self) -> WebConfig:
        return load_web_config()
