import typing

from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy import ForeignKey

from db.model import Base


class Chat(Base):
    __tablename__ = "chats"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    group_id = mapped_column(ForeignKey("groups.id"), nullable=False)
    group: Mapped["Group"] = relationship(back_populates="chat")
    messages: Mapped[typing.List["Message"]] = relationship(back_populates="chat")
