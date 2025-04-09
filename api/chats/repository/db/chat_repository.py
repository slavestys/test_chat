from sqlalchemy import select
from sqlalchemy.orm import load_only

from db.repository import BaseDbRepository
from groups.models import Group
from users.models import User

from ...models import Chat

from ..base import ChatRepositoryBase


class ChatRepository(ChatRepositoryBase, BaseDbRepository):
    async def find_by_id(self, chat_id):
        stmt = select(Chat).where(Chat.id == chat_id)
        return (await self.session.scalars(stmt)).one_or_none()

    async def find_user_chats(self, user_id):
        stmt = select(Chat).join(Group).join(Group.users).where(User.id == user_id)
        return (await self.session.scalars(stmt)).all()
