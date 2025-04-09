import typing

from fastapi import Depends

from . import db


chat_repository = typing.Annotated[db.ChatRepository, Depends()]

