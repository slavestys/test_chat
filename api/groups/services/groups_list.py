from typing import Annotated

from fastapi import Query

from db.seevice import BaseDBService
from db.dependencies import session_dependency

from ..schemas import GroupSearchSchema
from ..repository import groups_repository


class GroupsListService(BaseDBService):
    query: GroupSearchSchema
    groups: groups_repository

    def __init__(self, session: session_dependency, query: Annotated[GroupSearchSchema, Query()], groups: groups_repository):
        super(GroupsListService, self).__init__(session)
        self.query = query
        self.groups = groups

    def process(self):
        return self.groups.list(self.query)
