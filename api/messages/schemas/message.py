import uuid
import typing

from pydantic import BaseModel, Field


class MessageSchema(BaseModel):
    id: uuid.UUID = Field(..., description="Уникальный идентификатор сообщения")
    text: str = Field(..., description="Содержимое сообщения")
    chat_id: typing.Optional[int] = Field(default=None)
    user_id: typing.Optional[uuid.UUID] = Field(default=None)
