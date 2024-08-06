from abc import ABC, abstractmethod
from dataclasses import dataclass

from sqlalchemy import or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.entities.user import User as UserEntity
from src.infra.database.models.user import User as UserModel
from src.infra.database.converters import (
    convert_user_entity_to_user_model,
    convert_user_model_to_user_entity,
)


@dataclass
class BaseUserRepo(ABC):
    @abstractmethod
    async def create_new_user(self, user: UserEntity) -> None: ...

    @abstractmethod
    async def get_user_by_oid(self, oid: str) -> UserEntity | None: ...

    @abstractmethod
    async def get_user_by_username(self, username: str) -> UserEntity | None: ...

    @abstractmethod
    async def delete_user_by_oid(self, oid: str) -> None: ...

    @abstractmethod
    async def check_user_exist_by_email_or_username(
        self, email: str, username: str
    ) -> UserEntity | None: ...


@dataclass
class UserRepo(BaseUserRepo):
    _session: AsyncSession

    async def create_new_user(self, user: UserEntity) -> None:
        self._session.add(convert_user_entity_to_user_model(user))
        await self._session.commit()

    async def get_user_by_oid(self, oid: str) -> UserEntity | None:
        user = await self._session.get(UserModel, oid)
        if not user:
            return None
        return convert_user_model_to_user_entity(user)

    async def get_user_by_username(self, username: str) -> UserEntity | None:
        query = select(UserModel).where(UserModel.name == username)
        user = await self._session.scalar(query)
        if not user:
            return None
        return convert_user_model_to_user_entity(user)

    async def delete_user_by_oid(self, oid: str) -> None:
        user = await self._session.get(UserModel, oid)

        await self._session.delete(user)
        await self._session.commit()

    async def check_user_exist_by_email_or_username(
        self, email: str, username: str
    ) -> UserEntity | None:
        query = select(UserModel).where(
            or_(UserModel.email == email, UserModel.name == username)
        )

        user = await self._session.scalar(query)
        if not user:
            return None

        return convert_user_model_to_user_entity(user)
