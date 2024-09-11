from abc import ABC, abstractmethod
from dataclasses import dataclass

from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.entities.classified import Classified as ClassifiedEntity
from src.infra.database.models.classified import Classified as ClassifiedModel
from src.infra.database.converters import (
    convert_classified_entity_to_classified_model,
    convert_classified_model_to_classified_entity,
)


@dataclass
class BaseClassifiedRepo(ABC):
    @abstractmethod
    async def create_new_classified(self, classified: ClassifiedEntity) -> None: ...


@dataclass
class ClassifiedRepo(BaseClassifiedRepo):
    _session: AsyncSession

    async def create_new_classified(self, classified: ClassifiedEntity) -> None:
        self._session.add(convert_classified_entity_to_classified_model(classified))
        await self._session.commit()
