from dataclasses import dataclass

from src.domain.exceptions.base import ApplicationException


@dataclass(eq=False)
class UsernameTooShortException(ApplicationException):
    username: str

    @property
    def message(self):
        return f"Username '{self.username}' is too short"


@dataclass(eq=False)
class UsernameTooLongException(ApplicationException):
    username: str

    @property
    def message(self):
        return f"Username '{self.username[:50]}...' is too long"


@dataclass(eq=False)
class EmailInvalidException(ApplicationException):
    email: str

    @property
    def message(self):
        return f"Invalid email address '{self.email}'"
