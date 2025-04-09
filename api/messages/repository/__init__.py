import typing

from fastapi import Depends

from . import db


messages_repository = typing.Annotated[db.MessagesRepository, Depends()]

