from dataclasses import dataclass
from src.domain.exceptions.base import DomainException


@dataclass(eq=False)
class ApplicationException(DomainException):
    @property
    def message(self):
        return "An application error occurred."
