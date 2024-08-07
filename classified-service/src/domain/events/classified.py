from dataclasses import dataclass
from typing import ClassVar

from src.domain.events.base import BaseEvent


@dataclass
class NewClassifiedCreatedEvent(BaseEvent):
    event_title: ClassVar[str] = "Classified Created"

    classified_oid: str
    classified_title: str
    classified_description: str
    classified_price: float
    classified_owner_oid: str
