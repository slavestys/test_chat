import typing

from fastapi import Depends

from . import db


groups_repository = typing.Annotated[db.GroupsRepository, Depends()]

