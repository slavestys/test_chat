import typing

from db.seevice import BaseDBService
from db.dependencies import session_dependency
from fastapi import Query

from ..schemas import UserSearchSchema
from ..repository import users_repository
from ..authorization import require_current_user_dependency
from ..models import User


class SearchService(BaseDBService):
    query: UserSearchSchema
    users: users_repository
    user: User

    def __init__(
            self,
            query: typing.Annotated[UserSearchSchema, Query()],
            session: session_dependency,
            users: users_repository,
            user: require_current_user_dependency,
    ):
        super(SearchService, self).__init__(session)
        self.query = query
        self.users = users
        self.user = user

    def process(self):
        return self.users.list(self.query)
