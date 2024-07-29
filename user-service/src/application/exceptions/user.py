from dataclasses import dataclass

from src.application.exceptions.base import ApplicationException


@dataclass(eq=False)
class UserNotFoundException(ApplicationException):
    user_oid: str

    @property
    def message(self):
        return f"User with oid: {self.user_oid} has not been found."


@dataclass(eq=False)
class UsernameAlreadyExistsException(ApplicationException):
    username: str

    @property
    def message(self):
        return f"Username: {self.username} is already taken."


@dataclass(eq=False)
class EmailAlreadyExistsException(ApplicationException):
    email: str

    @property
    def message(self):
        return f"Email: {self.email} is already taken."
