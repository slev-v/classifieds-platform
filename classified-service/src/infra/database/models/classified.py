from sqlalchemy.orm import Mapped, mapped_column

from src.infra.database.models.base import Base


class Classified(Base):
    __tablename__ = "classifieds"
    __mapper_args__ = {"eager_defaults": True}

    oid: Mapped[str] = mapped_column(
        "oid", primary_key=True, unique=True, nullable=False
    )
    title: Mapped[str] = mapped_column("title", nullable=False)
    description: Mapped[str] = mapped_column("description", nullable=False)
    price: Mapped[float] = mapped_column("price", nullable=False)
    owner_oid: Mapped[str] = mapped_column("owner_oid", nullable=False)
    is_active: Mapped[bool] = mapped_column("is_active", nullable=False, default=True)
