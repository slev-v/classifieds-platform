from pydantic import BaseModel

from src.domain.entities.classified import Classified


class CreateClassifiedRequestSchema(BaseModel):
    title: str
    description: str
    price: float
    owner_oid: str
    is_active: bool


class CreateClassifiedResponseSchema(BaseModel):
    oid: str
    title: str
    description: str
    price: float
    owner_oid: str
    is_active: bool

    @classmethod
    def from_entity(cls, classified: Classified) -> "CreateClassifiedResponseSchema":
        return cls(
            oid=classified.oid,
            title=classified.title,
            description=classified.description,
            price=classified.price,
            owner_oid=classified.owner_oid,
            is_active=classified.is_active,
        )
