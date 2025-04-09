import abc


class BaseService(abc.ABC):
    @abc.abstractmethod
    async def process(self):
        raise NotImplementedError()
