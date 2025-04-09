import uuid

from pydantic import BaseModel, Field


class RegistrationSchema(BaseModel):
    name: str = Field(max_length=255)
    email: str = Field(max_length=255)
    password: str = Field(max_length=255)


class UserGetSchema(BaseModel):
    id: uuid.UUID
    name: str = Field(max_length=255)
    email: str = Field(max_length=255)


class GetTokenSchema(BaseModel):
    email: str = Field(max_length=255)
    password: str = Field(max_length=255)


class TokenSchema(BaseModel):
    token: str
    chat_ids: list[int]


class UserSearchSchema(BaseModel):
    name: str


