import abc

from ...schemas import GroupCreateSchema, GroupSearchSchema


class GroupsRepositoryBase(abc.ABC):
    @abc.abstractmethod
    async def find_by_chat_id(self, chat_id: int):
        raise NotImplementedError()

    @abc.abstractmethod
    async def find_by_group_id(self, group_id: int):
        raise NotImplementedError()

    @abc.abstractmethod
    async def find_private_by_user_ids(self, user_ids):
        raise NotImplementedError()

    @abc.abstractmethod
    async def create(self, create_data: GroupCreateSchema, group_type: int):
        raise NotImplementedError()

    @abc.abstractmethod
    async def join(self, group):
        raise NotImplementedError()

    @abc.abstractmethod
    async def list(self, query: GroupSearchSchema):
        raise NotImplementedError()
