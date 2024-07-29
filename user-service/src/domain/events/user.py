from dataclasses import dataclass
from typing import ClassVar

from src.domain.events.base import BaseEvent


@dataclass
class NewUserCreatedEvent(BaseEvent):
    event_title: ClassVar[str] = "User Created"

    user_oid: str
    user_name: str
    user_email: str


@dataclass
class UserDeletedEvent(BaseEvent):
    event_title: ClassVar[str] = "User Deleted"

    user_oid: str
