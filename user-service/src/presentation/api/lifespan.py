from src.infra.message_brokers.base import BaseMessageBroker
from src.presentation.api.config import WebConfig
from src.presentation.api.di import init_container
from src.application.mediator.base import Mediator
from src.application.events.test_event import TestEvent


async def init_message_broker():
    container = init_container()
    message_broker: BaseMessageBroker = await container.get(BaseMessageBroker)
    await message_broker.start()


async def consume_in_background():
    container = init_container()
    config: WebConfig = await container.get(WebConfig)
    message_broker: BaseMessageBroker = await container.get(BaseMessageBroker)

    mediator: Mediator = await container.get(Mediator)

    # async for msg in message_broker.start_consuming("test-topic"):
    #     await mediator.publish(
    #         [
    #             TestEvent(
    #                 test_id=msg["test_id"],
    #                 test_name=msg["test_name"],
    #                 test_description=msg["test_description"],
    #             ),
    #         ]
    #     )


async def close_message_broker():
    container = init_container()
    message_broker: BaseMessageBroker = await container.get(BaseMessageBroker)
    await message_broker.close()
