import typing

from sqlalchemy import select, column, and_
from sqlalchemy.orm import selectinload, aliased

from db.repository import BaseDbRepository
from db.dependencies import session_dependency
from users.authorization import require_current_user_dependency
from chats.models import Chat
from users.models import User

from ...schemas import GroupCreateSchema
from ...models import Group, GroupUser
from ...const import GroupType
from ...schemas import GroupSearchSchema

from ..base import GroupsRepositoryBase


class GroupsRepository(GroupsRepositoryBase, BaseDbRepository):
    def __init__(self, session: session_dependency, user: require_current_user_dependency):
        super(GroupsRepository, self).__init__(session)
        self.user = user

    async def find_by_chat_id(self, chat_id: int):
        stmt = (
            self.base_group_query
            .join(Group.chat)
            .where(Chat.id == chat_id)
        )
        return (await self.session.scalars(stmt)).one_or_none()

    async def find_by_group_id(self, group_id: int):
        stmt = (
            self.base_group_query
            .where(Group.id == group_id)
        )
        return (await self.session.scalars(stmt)).one_or_none()

    async def find_private_by_user_ids(self, user_ids):
        user1_table = aliased(GroupUser, name="users1")
        user2_table = aliased(GroupUser, name="users2")
        group_stmt = (
            self.base_group_query
            .join(user1_table)
            .join(user2_table)
            .where(Group.group_type == GroupType.private)
            .where(user1_table.user_id == user_ids[0])
            .where(user2_table.user_id == user_ids[1])
        )
        group = (await self.session.scalars(group_stmt)).one_or_none()
        return group

    async def create(self, create_data: GroupCreateSchema, group_type: int):
        users = await self._get_users_to_add(create_data.user_ids)
        group = Group(name=create_data.name, creator=self.user, group_type=group_type)
        self.session.add(group)
        chat = Chat(group=group)
        self.session.add(chat)
        for user in users:
            group.users.append(user)
        await self.session.commit()
        return group

    async def list(self, query: GroupSearchSchema, page_size=10):
        stmt = self.base_group_query.where(Group.group_type == GroupType.public)
        if query.name:
            stmt = stmt.where(column("name").ilike(f"{query.name}%"))
        stmt = stmt.limit(page_size).order_by(Group.id.desc())
        groups = (await self.session.scalars(stmt)).all()
        return groups

    async def join(self, group):
        group.users.append(self.user)
        await self.session.commit()

    async def _get_users_to_add(self, user_ids) -> typing.List[User]:
        to_add = {}
        if user_ids:
            stmt = select(User).where(User.id.in_(user_ids))
            users = (await self.session.scalars(stmt)).all()
            for user in users:
                to_add[user.id] = user
        to_add[self.user.id] = self.user
        return list(to_add.values())

    @property
    def base_group_query(self):
        return (
            select(Group)
            .options(
                selectinload(Group.chat),
                selectinload(Group.creator),
                selectinload(Group.users),
            )
        )