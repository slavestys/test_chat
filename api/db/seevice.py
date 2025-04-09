import abc

from sqlalchemy.ext.asyncio import AsyncSession

from core.seevice import BaseService

from .dependencies import session_dependency


class BaseDBService(BaseService, abc.ABC):
    session: AsyncSession

    def __init__(self, session: session_dependency):
        self.session = session