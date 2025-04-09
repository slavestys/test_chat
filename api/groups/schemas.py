import uuid

from pydantic import BaseModel, Field

from users.schemas import UserGetSchema
from chats.schemas import ChatGetSchema


class GroupCreateSchema(BaseModel):
    name: str = Field(max_length=255)
    user_ids: list[uuid.UUID]


class GroupGetSchema(BaseModel):
    id: int
    name: str
    creator: UserGetSchema
    users: list[UserGetSchema]
    chat: ChatGetSchema


class GroupSearchSchema(BaseModel):
    name: str | None


class GroupJoinSchema(BaseModel):
    group_id: int
