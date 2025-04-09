import uuid

from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy import Text, ForeignKey

from db.model import Base
from users.models import User


class Message(Base):
    __tablename__ = "messages"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True)
    text: Mapped[str] = mapped_column(Text)
    sender_id = mapped_column(ForeignKey("users.id"), nullable=False)
    sender: Mapped[User] = relationship(back_populates="messages")
    chat_id: Mapped[int] = mapped_column(ForeignKey("chats.id"), nullable=False)
    chat: Mapped["Chat"] = relationship(back_populates="messages")
    timestamp: Mapped[int]