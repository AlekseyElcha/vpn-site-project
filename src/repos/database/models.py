import uuid
from typing import List
from sqlalchemy import text, BigInteger, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
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
    tg_id: Mapped[int] = mapped_column(
        BigInteger,
        unique=True,
        index=True,
        nullable=False
    )
    balance: Mapped[float] = mapped_column(
        BigInteger,
        nullable=False,
        index=True
    )
    clients: Mapped[List["ClientModel"]] = relationship(
        "ClientModel",
        back_populates="user",
        cascade="all, delete-orphan"
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
    creation_time: Mapped[int] = mapped_column(
        BigInteger,
        nullable=False,
        index=True
    )
    tg_id: Mapped[int] = mapped_column(
        ForeignKey("users.tg_id", ondelete="CASCADE"),
        index=True,
        nullable=False
    )
    total_gb: Mapped[int] = mapped_column(BigInteger)
    expiry_time: Mapped[int] = mapped_column(
        BigInteger,
        nullable=False,
        index=True
    )
    enable: Mapped[bool] = mapped_column()

    user: Mapped["UserModel"] = relationship("UserModel", back_populates="clients")


class PaymentModel(Base):
    __tablename__ = "payments"

    id: Mapped[uuid.UUID] = mapped_column(
        SQLAUUID(as_uuid=True),
        primary_key=True,
        server_default=text("gen_random_uuid()")
    )
    tg_id: Mapped[int] = mapped_column(
        BigInteger,
        nullable=False,
        index=True
    )
    item_id: Mapped[str] = mapped_column(
        nullable=False,
        index=True
    )
    time: Mapped[int] = mapped_column(
        BigInteger,
        nullable=False,
    )
    amount: Mapped[int] = mapped_column(
        nullable=False
    )

