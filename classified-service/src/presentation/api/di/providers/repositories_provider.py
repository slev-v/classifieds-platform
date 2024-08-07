from dishka import Provider, provide, Scope

from sqlalchemy.ext.asyncio import AsyncSession

from src.infra.database.repositories.classified import (
    ClassifiedRepo,
    BaseClassifiedRepo,
)


class RepositoriesProvider(Provider):
    @provide(scope=Scope.REQUEST)
    def get_classified_repo(self, session: AsyncSession) -> BaseClassifiedRepo:
        return ClassifiedRepo(_session=session)
