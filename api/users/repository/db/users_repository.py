import uuid

from sqlalchemy import select, column

from db.repository import BaseDbRepository

from ...schemas import UserSearchSchema
from ...models import User

from ..base import UsersRepositoryBase


class UsersRepository(UsersRepositoryBase, BaseDbRepository):
    async def find_by_email(self, email):
        return (await self.session.scalars(select(User).where(User.email == email))).one_or_none()

    async def create(self, **kwargs):
        user = User(
            id=uuid.uuid4(),
            **kwargs,
        )
        self.session.add(user)
        await self.session.commit()
        return user

    async def list(self, query: UserSearchSchema, page_size=10):
        stmt = select(User)
        if query.name:
            stmt = stmt.where(column("name").ilike(f"{query.name}%"))
        stmt = stmt.limit(page_size).order_by(User.id.desc())
        users = (await self.session.scalars(stmt)).all()
        return users
