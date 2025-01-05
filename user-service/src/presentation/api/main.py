from contextlib import asynccontextmanager
from fastapi import FastAPI
from dishka.integrations.fastapi import setup_dishka as setup_dishka_fastapi

from src.infra.message_brokers.base import BaseMessageBroker
from src.presentation.api.di import init_container
from src.presentation.api.user.handlers import router as user_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    message_broker: BaseMessageBroker = await app.state.container.get(BaseMessageBroker)

    await message_broker.start()

    yield
    await message_broker.stop()


def create_app() -> FastAPI:
    app = FastAPI(
        title="User Service",
        debug=True,
        lifespan=lifespan,
    )

    container = init_container()
    app.state.container = container
    setup_dishka_fastapi(container, app)

    app.include_router(user_router)

    return app
