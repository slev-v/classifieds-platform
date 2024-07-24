from fastapi import APIRouter
from dishka.integrations.fastapi import FromDishka, inject

from src.application.mediator.base import Mediator
from src.application.commands.test import TestCommand
from src.infra.message_brokers.base import BaseMessageBroker

router = APIRouter()


@router.get("/")
async def check_health():
    return {"message": "Hello World"}


@router.get("/test")
@inject
async def test(mediator: FromDishka[Mediator]):
    await mediator.handle_command(TestCommand("1", "test", "test"))
    return {"message": "Test command handled"}


@router.get("/producer_status")
@inject
async def producer_status(message_broker: FromDishka[BaseMessageBroker]):
    return {"producer_status": message_broker.producer_started}
