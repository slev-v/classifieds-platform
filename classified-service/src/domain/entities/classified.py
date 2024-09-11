from dataclasses import dataclass

from src.domain.entities.base import BaseEntity
from src.domain.events.classified import NewClassifiedCreatedEvent


@dataclass(eq=False)
class Classified(BaseEntity):
    title: str
    description: str
    price: float
    owner_oid: str
    is_active: bool

    @classmethod
    def create_classified(
        cls, title: str, description: str, price: float, owner_oid: str
    ) -> "Classified":
        new_classified = cls(
            title=title,
            description=description,
            price=price,
            owner_oid=owner_oid,
            is_active=True,
        )
        new_classified.register_event(
            NewClassifiedCreatedEvent(
                classified_oid=new_classified.oid,
                classified_title=new_classified.title,
                classified_description=new_classified.description,
                classified_price=new_classified.price,
                classified_owner_oid=new_classified.owner_oid,
            )
        )
        return new_classified

    # def update(self, title: str, description: str, price: float):
    #     self.title = title
    #     self.description = description
    #     self.price = price
    #     self.register_event(
    #         ClassifiedUpdatedEvent(
    #             classified_oid=self.oid,
    #             classified_title=self.title,
    #             classified_description=self.description,
    #             classified_price=self.price,
    #         )
    #     )
    # def activate(self):
    #     self.is_active = True
    #     self.register_event(ClassifiedActivatedEvent(classified_oid=self.oid))
    # def deactivate(self):
    #     self.is_active = False
    #     self.register_event(ClassifiedDeactivatedEvent(classified_oid=self.oid))
