import typing
from http import HTTPStatus

from fastapi import Path
from fastapi.exceptions import HTTPException

from db.seevice import BaseDBService
from db.dependencies import session_dependency
from users.models import User
from broker.producer import producer
from users.authorization import require_current_user_dependency

from ..const import GroupType
from ..repository import groups_repository


class GroupJoinService(BaseDBService):
    user: User
    groups: groups_repository
    group_id: int

    def __init__(
            self,
            session: session_dependency,
            group_id: typing.Annotated[int, Path()],
            groups: groups_repository,
            user: require_current_user_dependency,
         ):
        super(GroupJoinService, self).__init__(session)
        self.group_id = group_id
        self.groups = groups
        self.user = user

    async def process(self):
        group = await self.groups.find_by_group_id(self.group_id)
        if group.group_type != GroupType.public:
            raise HTTPException(
                status_code=HTTPStatus.FORBIDDEN,
                detail={"type": "access_denied"}
            )
        if group.is_member(self.user):
            return group
        await self.groups.join(group)
        await producer.send_message(
            topic="messages",
            message_type="chat_join",
            message={
                "user_id": str(self.user.id),
                "chat_id": group.chat.id,
            }
        )
        return group
