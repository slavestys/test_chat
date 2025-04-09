from typing import Annotated

from fastapi import Query

from db.seevice import BaseDBService
from db.dependencies import session_dependency
from users.authorization import require_current_user_dependency

from ..schemas import MessageSearch
from ..repository import messages_repository


class MessageSearchService(BaseDBService):
    query: MessageSearch
    messages: messages_repository

    def __init__(
            self,
            session: session_dependency,
            query: Annotated[MessageSearch, Query()],
            user: require_current_user_dependency,
            messages: messages_repository,
    ):
        super(MessageSearchService, self).__init__(session)
        self.query = query
        self.user = user
        self.messages = messages

    def process(self):
        return self.messages.list(self.query)