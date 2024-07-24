from pydantic import BaseModel

from src.domain.entities.user import User


class CreateUserRequestSchema(BaseModel):
    username: str
    email: str


class CreateUserResponseSchema(BaseModel):
    oid: str
    username: str
    email: str

    @classmethod
    def from_entity(cls, user: User) -> "CreateUserResponseSchema":
        return cls(
            oid=user.oid,
            username=user.name.as_generic_type(),
            email=user.email.as_generic_type(),
        )
