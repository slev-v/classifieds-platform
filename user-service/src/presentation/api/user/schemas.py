from pydantic import BaseModel

from src.domain.entities.user import User


class CreateUserRequestSchema(BaseModel):
    username: str
    email: str
    password: str


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


class LoginUserRequestSchema(BaseModel):
    username: str
    password: str


class LoginUserResponseSchema(BaseModel):
    session_oid: str


class GetUserByOidResponseSchema(BaseModel):
    oid: str
    username: str
    email: str

    @classmethod
    def from_entity(cls, user: User) -> "GetUserByOidResponseSchema":
        return cls(
            oid=user.oid,
            username=user.name.as_generic_type(),
            email=user.email.as_generic_type(),
        )
