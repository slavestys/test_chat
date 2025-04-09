from db.seevice import BaseDBService
from db.dependencies import session_dependency
from users.models import User
from broker.producer import producer
from users.authorization import require_current_user_dependency

from ..schemas import GroupCreateSchema
from ..const import GroupType
from ..repository import groups_repository



class GroupCreateService(BaseDBService):
    create_data: GroupCreateSchema
    user: User
    groups: groups_repository

    def __init__(self,
                 session: session_dependency,
                 create_data: GroupCreateSchema,
                 groups: groups_repository,
                 user: require_current_user_dependency,
        ):
        super(GroupCreateService, self).__init__(session)
        self.create_data = create_data
        self.groups = groups
        self.user = user

    async def process(self):
        group = await self.groups.create(self.create_data, GroupType.public)
        await producer.send_message(
            topic="messages",
            message_type="chat_join",
            message={
                "user_id": str(self.user.id),
                "chat_id": group.chat.id,
            }
        )
        return group
