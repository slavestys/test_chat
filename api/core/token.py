from datetime import datetime, timezone

import jwt
from jwt.exceptions import InvalidTokenError

import settings


def create_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + settings.TOKEN_EXPIRATION
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.TOKEN_SECRET_KEY, algorithm=settings.TOKEN_ALGORITHM)
    return encoded_jwt


def get_token_payload(token):
    try:
        return jwt.decode(token, settings.TOKEN_SECRET_KEY, algorithms=[settings.TOKEN_ALGORITHM])
    except InvalidTokenError:
        return {}
