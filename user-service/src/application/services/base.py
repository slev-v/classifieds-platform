from abc import ABC, abstractmethod

from dataclasses import dataclass


@dataclass
class BaseHasherPasswordService(ABC):
    @abstractmethod
    def get_password_hash(self, password: str) -> str: ...

    @abstractmethod
    def verify_password(self, plain_password: str, hashed_password: str) -> bool: ...


@dataclass
class BaseSessionService(ABC):
    @abstractmethod
    async def create_session(self, session_oid: str, user_oid: str) -> None: ...

    @abstractmethod
    async def delete_session(self, session_oid: str) -> None: ...

    @abstractmethod
    async def get(self, session_oid: str) -> str: ...
