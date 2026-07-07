import datetime
from typing import Literal, Optional

from sqlalchemy import (
    BigInteger,
    CheckConstraint,
    DateTime,
    ForeignKey,
    String,
    Text,
    func,
)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    """Базовый класс для всех моделей."""

    pass


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    telegram_id: Mapped[int] = mapped_column(BigInteger, unique=True, nullable=False)
    username: Mapped[Optional[str]] = mapped_column(String(255))

    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(
        DateTime(timezone=True), onupdate=func.now()
    )

    messages: Mapped[list["Message"]] = relationship(
        back_populates="user", cascade="all, delete-orphan"
    )
    requests: Mapped[list["Request"]] = relationship(
        back_populates="user", cascade="all, delete-orphan"
    )


class Message(Base):
    __tablename__ = "messages"

    message_id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    message_text: Mapped[str] = mapped_column(Text, nullable=False)
    bot_answer: Mapped[Optional[str]] = mapped_column(Text)

    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(
        DateTime(timezone=True), onupdate=func.now()
    )

    feedback: Mapped[Optional[Literal["like", "dislike"]]] = mapped_column(String(7))
    category: Mapped[Optional[str]] = mapped_column(String(100))
    error: Mapped[Optional[str]] = mapped_column(Text)

    user: Mapped["User"] = relationship(back_populates="messages")

    __table_args__ = (
        CheckConstraint("feedback IN ('like', 'dislike')", name="check_feedback_types"),
    )


class Request(Base):
    __tablename__ = "requests"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )

    status: Mapped[Literal["pending", "sent", "completed", "cancelled"]] = (
        mapped_column(String(20), nullable=False)
    )
    desired_datetime: Mapped[Optional[datetime.datetime]] = mapped_column(
        DateTime(timezone=True)
    )

    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[Optional[datetime.datetime]] = mapped_column(
        DateTime(timezone=True), onupdate=func.now()
    )

    user: Mapped["User"] = relationship(back_populates="requests")

    __table_args__ = (
        CheckConstraint(
            "status IN ('pending', 'sent', 'completed', 'cancelled')",
            name="check_request_status",
        ),
    )
