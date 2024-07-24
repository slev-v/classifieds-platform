from dataclasses import dataclass
import re

from src.domain.values.base import BaseValueObject
from src.domain.exceptions.user import (
    UsernameTooShortException,
    UsernameTooLongException,
    EmailInvalidException,
)


@dataclass(frozen=True)
class Username(BaseValueObject[str]):
    def validate(self):
        if len(self.value) < 3:
            raise UsernameTooShortException(username=self.value)
        if len(self.value) > 50:
            raise UsernameTooLongException(username=self.value)

    def as_generic_type(self) -> str:
        return str(self.value)


@dataclass(frozen=True)
class Email(BaseValueObject[str]):
    def validate(self):
        regex = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"

        if not re.fullmatch(regex, self.value):
            raise EmailInvalidException(email=self.value)

    def as_generic_type(self) -> str:
        return str(self.value)
