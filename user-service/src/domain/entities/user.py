from dataclasses import dataclass

from src.domain.entities.base import BaseEntity
from src.domain.events.user import NewUserCreatedEvent
from src.domain.values.user import Username, Email


@dataclass(eq=False)
class User(BaseEntity):
    name: Username
    email: Email
    hashed_password: str

    @classmethod
    def create_user(cls, name: Username, email: Email, hashed_password: str) -> "User":
        new_user = cls(name=name, email=email, hashed_password=hashed_password)
        new_user.register_event(
            NewUserCreatedEvent(
                user_oid=new_user.oid,
                user_name=new_user.name.as_generic_type(),
                user_email=new_user.email.as_generic_type(),
            )
        )

        return new_user

    # def user_event_call(self):
    #     self.register_event(
    #         TestEvent(
    #             test_id=self.user_id,
    #             test_name=self.user_name,
    #             test_description=self.user_email,
    #         )
    #     )

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


@dataclass(eq=False)
class Test(BaseEntity):
    test_id: str
    test_name: str
    test_description: str

    def test_event_call(self):
        self.register_event(
            TestEvent(
                test_id=self.test_id,
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
