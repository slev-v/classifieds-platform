from src.domain.entities.user import User as UserEntity
from src.domain.values.user import Email, Username
from src.infra.database.models.user.user import User as UserModel


def convert_user_entity_to_user_model(user: UserEntity) -> UserModel:
    return UserModel(
        oid=user.oid,
        name=user.name.as_generic_type(),
        email=user.email.as_generic_type(),
        hashed_password=user.hashed_password,
    )


def convert_user_model_to_user_entity(user: UserModel) -> UserEntity:
    return UserEntity(
        oid=user.oid,
        name=Username(user.name),
        email=Email(user.email),
        hashed_password=user.hashed_password,
    )
