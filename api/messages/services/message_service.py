from http import HTTPStatus

from fastapi.exceptions import HTTPException

from db.seevice import BaseDBService
from db.dependencies import session_dependency
from users.authorization import require_current_user_dependency
from chats.repository import chat_repository
from groups.schemas import GroupCreateSchema
from groups.const import GroupType
from groups.repository import groups_repository
from broker.producer import producer

from ..schemas import MessageSchema
from ..repository import messages_repository


class MessageService(BaseDBService):
    create_data: MessageSchema
    messages: messages_repository
    chats: chat_repository
    groups: groups_repository

    def __init__(
            self,
            session: session_dependency,
            create_data: MessageSchema,
            user: require_current_user_dependency,
            messages: messages_repository,
            chats: chat_repository,
            groups: groups_repository,
    ):
        super(MessageService, self).__init__(session)
        self.create_data = create_data
        self.user = user
        self.messages = messages
        self.chats = chats
        self.groups = groups

    async def process(self):
        group = await self._get_group()
        if not group:
            raise HTTPException(
                status_code=HTTPStatus.UNPROCESSABLE_ENTITY,
                detail={"type": "not-found", "loc": ["chat"]}
            )
        if not group.is_member(self.user):
            raise HTTPException(
                status_code=HTTPStatus.UNPROCESSABLE_ENTITY,
                detail={"type": "not-member", "loc": ["chat"]}
            )
        message = await self.messages.create(
            create_data=self.create_data,
            user=self.user,
            chat=group.chat,
        )
        await producer.send_message(
            topic="messages",
            message_type="message",
            message={
                "text": message.text,
                "sender_id": str(message.sender_id),
                "chat_id": str(message.chat_id),
            }
        )
        return message

    async def _get_group(self):
        if self.create_data.chat_id:
            return await self.groups.find_by_chat_id(self.create_data.chat_id)
        elif self.create_data.user_id:
            user_ids = (self.user.id, self.create_data.user_id)
            group = await self.groups.find_private_by_user_ids(user_ids)
            if group:
                return group
            group_create_data = GroupCreateSchema(
                name=f"private_{self.user.id}_{self.create_data.user_id}",
                user_ids=user_ids
            )
            group = await self.groups.create(group_create_data, group_type=GroupType.private)
            return group
        else:
            return None


