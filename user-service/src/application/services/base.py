from abc import ABC, abstractmethod

from dataclasses import dataclass


@dataclass
class BaseHasherPasswordService(ABC):
    @abstractmethod
    def get_password_hash(self, password: str) -> str: ...

    @abstractmethod
    def verify_password(self, plain_password: str, hashed_password: str) -> bool: ...


# from typing import Protocol
#
#
# class HasherPassword(Protocol):
#     def get_password_hash(self, password: str) -> str:
#         raise NotImplementedError
#
#     def verify_password(self, plain_password: str, hashed_password: str) -> bool:
#         raise NotImplementedError
