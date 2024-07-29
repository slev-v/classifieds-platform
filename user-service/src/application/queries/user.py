from dataclasses import dataclass

from src.application.exceptions.user import UserNotFoundException
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


# @dataclass(frozen=True)
# class GetAllChatsListenersQuery(BaseQuery):
#     chat_oid: str
#
# @dataclass(frozen=True)
# class GetAllChatsQueryHandler(BaseQueryHandler[GetAllChatsQuery, Iterable[Chat]]):
#     chats_repository: BaseChatsRepository
#
#     async def handle(self, query: GetAllChatsQuery) -> Iterable[Chat]:  # type: ignore
#         return await self.chats_repository.get_all_chats(filters=query.filters)
