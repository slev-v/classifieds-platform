from dataclasses import dataclass

from src.application.exceptions.user import InvalidSessionId
from src.presentation.api.config import WebConfig
from src.infra.redis.repositories.base import BaseRedisRepository

import bcrypt

from src.application.services.base import BaseHasherPasswordService, BaseSessionService


@dataclass
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


@dataclass
class SessionService(BaseSessionService):
    config: WebConfig
    redis_repo: BaseRedisRepository

    async def create_session(self, session_oid: str, user_oid: str) -> None:
        ex_seconds = self.config.session_expire_time * 60
        await self.redis_repo.set_with_ex(session_oid, user_oid, ex_seconds)

    async def delete_session(self, session_oid: str) -> None:
        await self.redis_repo.delete(session_oid)

    async def get(self, session_oid: str) -> str:
        user_oid_bytes = await self.redis_repo.get(session_oid)
        if not user_oid_bytes:
            raise InvalidSessionId
        user_oid = user_oid_bytes.decode("utf-8")
        return user_oid
