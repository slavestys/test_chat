from sqlalchemy.ext.asyncio import AsyncSession

from .dependencies import session_dependency


class BaseDbRepository:
    session: AsyncSession

    def __init__(self, session: session_dependency):
        self.session = session
