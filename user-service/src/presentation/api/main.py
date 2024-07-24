from contextlib import asynccontextmanager
from fastapi import FastAPI
from dishka.integrations.fastapi import setup_dishka

from src.presentation.api.di import init_container
from src.presentation.api.v1.main import router
from src.presentation.api.user.handlers import router as user_router
from src.presentation.api.config import load_web_config
from src.presentation.api.lifespan import close_message_broker, init_message_broker
from src.infra.message_brokers.base import BaseMessageBroker


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_message_broker()

    # container = container_factory()

    # scheduler: Scheduler = container.resolve(Scheduler)

    # job = await scheduler.spawn(consume_in_background())

    yield
    await close_message_broker()
    # await job.close()


def create_app() -> FastAPI:
    app = FastAPI(
        title="User Service",
        debug=True,
        lifespan=lifespan,
    )

    container = init_container()
    setup_dishka(container, app)
    app.include_router(router)
    app.include_router(user_router)

    return app
