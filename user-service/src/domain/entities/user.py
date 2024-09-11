from dataclasses import dataclass

from src.domain.entities.base import BaseEntity
from src.domain.events.user import (
    NewUserCreatedEvent,
    UserDeletedEvent,
    UserLoggedInEvent,
    UserLoggedOutEvent,
)
from src.domain.values.user import Username, Email


@dataclass(eq=False)
class Session(BaseEntity):
    user_oid: str


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

    def delete(self):
        self.register_event(UserDeletedEvent(user_oid=self.oid))

    def login(self, session_oid: str):
        self.register_event(
            UserLoggedInEvent(
                user_oid=self.oid,
                session_oid=session_oid,
            )
        )

    def logout(self, session_oid: str):
        self.register_event(
            UserLoggedOutEvent(user_oid=self.oid, session_oid=session_oid)
        )
