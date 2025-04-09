import uuid
import typing

from db.model import Base

from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy import String


class User(Base):
    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255))
    email: Mapped[str] = mapped_column(String(255), unique=True)
    password: Mapped[str] = mapped_column(String(255))
    messages: Mapped[typing.List["Message"]] = relationship(back_populates="sender")
    created_groups: Mapped[typing.List["Group"]] = relationship(back_populates="creator")
    groups: Mapped[typing.List["Group"]] = relationship(
        back_populates="users",
        secondary="groups_users",
    )