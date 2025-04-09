import abc


class ChatRepositoryBase(abc.ABC):
    @abc.abstractmethod
    async def find_by_id(self, chat_id):
        raise NotImplementedError()
