from dataclasses import dataclass

from src.domain.exceptions.base import DomainException


@dataclass(eq=False)
class UsernameTooShortException(DomainException):
    username: str

    @property
    def message(self):
        return f"Username '{self.username}' is too short"


@dataclass(eq=False)
class UsernameTooLongException(DomainException):
    username: str

    @property
    def message(self):
        return f"Username '{self.username[:50]}...' is too long"


@dataclass(eq=False)
class EmailInvalidException(DomainException):
    email: str

    @property
    def message(self):
        return f"Invalid email address '{self.email}'"


@dataclass(eq=False)
class WrongPasswordException(DomainException):
    exception_text: str

    @property
    def message(self):
        return self.exception_text
