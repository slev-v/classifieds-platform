from dataclasses import dataclass

from src.domain.entities.base import BaseEntity
from src.application.events.test_event import TestEvent


@dataclass(eq=False)
class Test(BaseEntity):
    test_name: str
    test_description: str

    def test_event_call(self):
        self.register_event(
            TestEvent(
                test_name=self.test_name,
                test_description=self.test_description,
            )
        )

    # @classmethod
    # def create_chat(cls, title: Title) -> "Chat":
    #     new_chat = cls(title=title)
    #     new_chat.register_event(
    #         NewChatCreatedEvent(
    #             chat_oid=new_chat.oid, chat_title=new_chat.title.as_generic_type()
    #         )
    #     )
    #
    #     return new_chat
    #
    # def add_message(self, message: Message):
    #     self.messages.add(message)
    #     self.register_event(
    #         NewMessageReceivedEvent(
    #             message_text=message.text.as_generic_type(),
    #             chat_oid=self.oid,
    #             message_oid=message.oid,
    #         ),
    #     )
    #
    # def delete(self):
    #     self.is_deleted = True
    #     self.register_event(ChatDeletedEvent(chat_oid=self.oid))
    #
    # def add_listener(self, listener: ChatListener):
    #     if listener in self.listeners:
    #         raise ListenerAlreadyExistsException(listener_oid=listener.oid)
    #
    #     self.listeners.add(listener)
    #     self.register_event(ListenerAddedEvent(listener_oid=listener.oid))
