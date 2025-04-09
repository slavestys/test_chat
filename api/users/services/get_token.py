from http import HTTPStatus

from sqlalchemy import select
from fastapi.exceptions import HTTPException

from db.seevice import BaseDBService
from db.dependencies import session_dependency
from core.token import create_token
from chats.repository import chat_repository

from ..schemas import GetTokenSchema, TokenSchema
from ..models import User
from ..password import verify_password


class GetTokenService(BaseDBService):
    data: GetTokenSchema
    chats: chat_repository

    def __init__(self, data: GetTokenSchema, session: session_dependency, chats: chat_repository):
        super(GetTokenService, self).__init__(session)
        self.data = data
        self.chats = chats

    async def process(self):
        stmt = select(User).where(User.email == self.data.email)
        user = (await self.session.scalars(stmt)).one_or_none()
        if not user:
            self.raise_exception()
        if not verify_password(self.data.password, user.password):
            self.raise_exception()
        chats = await self.chats.find_user_chats(user.id)
        chat_ids = [chat.id for chat in chats]
        return TokenSchema(token=create_token({"sub": str(user.id)}), chat_ids=chat_ids)

    def raise_exception(self):
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED,
            detail={"type": "not-authorized"}
        )