from sqlalchemy import select
from datetime import datetime

from db.dependencies import session_dependency
from db.repository import BaseDbRepository
from groups.repository import groups_repository
from chats.repository import chat_repository
from users.models import User
from chats.models import Chat

from ...schemas import MessageSchema, MessageSearch
from ...models import Message

from ..base import MessagesRepositoryBase


class MessagesRepository(BaseDbRepository, MessagesRepositoryBase):
    groups: groups_repository
    chats: chat_repository

    def __init__(
            self,
            session: session_dependency,
            groups: groups_repository,
            chats: chat_repository
    ):
        super(MessagesRepository, self).__init__(session)
        self.groups = groups
        self.chats = chats

    async def create(self, create_data: MessageSchema, user: User, chat: Chat) -> Message:
        stmt = select(Message).where(Message.id == create_data.id)
        message = (await self.session.scalars(stmt)).one_or_none()
        if message:
            return message
        message = Message(
            id=create_data.id,
            text=create_data.text,
            sender=user,
            chat=chat,
            timestamp=int(datetime.now().timestamp()),
        )
        self.session.add(message)
        await self.session.commit()
        return message

    async def list(self, query: MessageSearch):
        stmt = select(Message)
        if query.chat_id:
            stmt = stmt.where(Message.chat_id == query.chat_id)
        stmt = stmt.order_by(Message.id.desc())
        return (await self.session.scalars(stmt)).all()


