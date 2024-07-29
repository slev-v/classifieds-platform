from dataclasses import dataclass

import bcrypt

from src.application.services.base import BaseHasherPasswordService


@dataclass()
class HasherPasswordService(BaseHasherPasswordService):
    def __init__(self) -> None:
        self._rounds = 12

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return bcrypt.checkpw(
            plain_password.encode("utf-8"), hashed_password.encode("utf-8")
        )

    def get_password_hash(self, password: str) -> str:
        salt = bcrypt.gensalt(self._rounds)
        hashed_password = bcrypt.hashpw(password.encode("utf-8"), salt)
        return hashed_password.decode("utf-8")
