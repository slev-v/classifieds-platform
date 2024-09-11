from abc import (
    ABC,
    abstractmethod,
)
from dataclasses import (
    dataclass,
    field,
)
from typing import Generic

from src.application.queries.base import (
    BaseQuery,
    BaseQueryHandler,
    QR,
    QT,
)


@dataclass(eq=False)
class QueryMediator(ABC, Generic[QT, QR]):
    queries_map: dict[QT, BaseQueryHandler] = field(
        default_factory=dict,
        kw_only=True,
    )

    @abstractmethod
    def register_query(
        self, query: QT, query_handler: BaseQueryHandler[QT, QR]
    ) -> None: ...

    @abstractmethod
    async def handle_query(self, query: BaseQuery) -> QR: ...
