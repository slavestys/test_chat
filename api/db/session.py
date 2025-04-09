import typing

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

import settings


engine = create_async_engine(settings.DATABASE_CONNECTION_STRING, echo=True)
session_maker = async_sessionmaker(engine, expire_on_commit=False)


async def get_session() -> typing.Generator[AsyncSession]:
    async with session_maker() as session:
        yield session
