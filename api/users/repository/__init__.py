import typing

from fastapi import Depends

from . import db


users_repository = typing.Annotated[db.UsersRepository, Depends()]

