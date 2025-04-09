from pydantic import BaseModel, Field


class MessageSearch(BaseModel):
    chat_id: int
