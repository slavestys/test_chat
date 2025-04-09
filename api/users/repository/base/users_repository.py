import abc

from ...schemas import UserSearchSchema


class UsersRepositoryBase(abc.ABC):
    @abc.abstractmethod
    async def find_by_email(self, email):
        raise NotImplementedError()

    @abc.abstractmethod
    async def create(self, **kwargs):
        raise NotImplementedError()

    @abc.abstractmethod
    async def list(self, query: UserSearchSchema):
        raise NotImplementedError()
