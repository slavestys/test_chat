import abc

from users.models import User
from chats.models import Chat

from ...schemas import MessageSchema, MessageSearch


class MessagesRepositoryBase(abc.ABC):
    @abc.abstractmethod
    async def create(self, create_data: MessageSchema, user: User, chat: Chat):
        raise NotImplementedError()

    @abc.abstractmethod
    async def list(self, query: MessageSearch):
        raise NotImplementedError()
