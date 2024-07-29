from sqlalchemy.orm import Mapped, mapped_column

from src.infra.database.models import Base


class User(Base):
    __tablename__ = "users"
    __mapper_args__ = {"eager_defaults": True}

    oid: Mapped[str] = mapped_column(
        "oid", primary_key=True, unique=True, nullable=False
    )
    name: Mapped[str] = mapped_column("name", nullable=False, unique=True)
    email: Mapped[str] = mapped_column("email", nullable=False, unique=True)
    hashed_password: Mapped[str] = mapped_column("hashed_password", nullable=False)
