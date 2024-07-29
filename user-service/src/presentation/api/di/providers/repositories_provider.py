from dishka import Provider, provide, Scope
from sqlalchemy.ext.asyncio import AsyncSession

from src.infra.database.repositories.user import UserRepo, BaseUserRepo


class RepositoriesProvider(Provider):
    @provide(scope=Scope.REQUEST)
    def get_user_repo(self, session: AsyncSession) -> BaseUserRepo:
        return UserRepo(_session=session)
