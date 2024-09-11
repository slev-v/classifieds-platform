from dataclasses import dataclass

from src.application.exceptions.user import UserNotFoundException
from src.application.services.base import BaseSessionService
from src.domain.entities.user import User
from src.application.queries.base import BaseQuery, BaseQueryHandler
from src.infra.database.repositories.user import BaseUserRepo


@dataclass(frozen=True)
class GetUserByOidQuery(BaseQuery):
    user_oid: str


@dataclass(frozen=True)
class GetUserByOidQueryHandler(BaseQueryHandler[GetUserByOidQuery, User]):
    user_repo: BaseUserRepo

    async def handle(self, query: GetUserByOidQuery) -> User:
        user = await self.user_repo.get_user_by_oid(query.user_oid)

        if not user:
            raise UserNotFoundException(user_oid=query.user_oid)

        return user


@dataclass(frozen=True)
class GetUserBySessionOidQuery(BaseQuery):
    session_oid: str


@dataclass(frozen=True)
class GetUserBySessionOidQueryHandler(BaseQueryHandler[GetUserBySessionOidQuery, User]):
    user_repo: BaseUserRepo
    session_service: BaseSessionService

    async def handle(self, query: GetUserBySessionOidQuery) -> User:
        user_oid = await self.session_service.get(query.session_oid)
        user = await self.user_repo.get_user_by_oid(oid=user_oid)

        if not user:
            raise UserNotFoundException(user_oid=user_oid)

        return user
