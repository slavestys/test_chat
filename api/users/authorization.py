from typing import Annotated
from http import HTTPStatus

from fastapi import Header, Depends
from sqlalchemy import select
from fastapi.exceptions import HTTPException

from core.token import get_token_payload
from db.dependencies import session_dependency

from .models import User


async def get_current_user(authorization: Annotated[str, Header()], session: session_dependency):
    if not authorization:
        return None
    token_parts = str(authorization).split(" ")
    token = token_parts[-1] if len(token_parts) == 2 else None
    if not token:
        return None
    payload = get_token_payload(token)
    user_id = payload.get("sub")
    if not user_id:
        return None
    stmt = select(User).where(User.id == user_id)
    return (await session.scalars(stmt)).one_or_none()


def require_current_user(user: Annotated[get_current_user, Depends()]):
    if user is None:
        raise HTTPException(status_code=HTTPStatus.UNAUTHORIZED, detail="not-authorized")
    return user


require_current_user_dependency = Annotated[require_current_user, Depends()]



