import uuid
from datetime import datetime

from sqlalchemy import text, DateTime, JSON
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, MappedSQLExpression
from sqlalchemy.dialects.postgresql import UUID as SQLAUUID


class Base(DeclarativeBase):
    pass

class UserModel(Base):
    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(
        SQLAUUID(as_uuid=True),
        primary_key=True,
        server_default=text("gen_random_uuid()"),
    )
    email: Mapped[str] = mapped_column(
        unique=True,
        index=True,
        nullable=False
    )
    tg_id: Mapped[int] = mapped_column(
        unique=True,
        index=True,
        nullable=True
    )



class ClientModel(Base):
    __tablename__ = "clients"

    id: Mapped[uuid.UUID] = mapped_column(
        SQLAUUID(as_uuid=True),
        primary_key=True,
        server_default=text("gen_random_uuid()"),
    )
    email: Mapped[str] = mapped_column(
        unique=True,
        index=True,
    )
    total_gb: Mapped[int] = mapped_column()
    expiry_time: Mapped[int] = mapped_column(
        nullable=False,
        index=True
    )
    enable: Mapped[bool] = mapped_column()
    inbounds: Mapped[list] = mapped_column(JSON, default=list)


