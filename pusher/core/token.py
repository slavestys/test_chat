import jwt
from jwt.exceptions import InvalidTokenError

import settings


def get_token_payload(token):
    try:
        return jwt.decode(token, settings.TOKEN_SECRET_KEY, algorithms=[settings.TOKEN_ALGORITHM])
    except InvalidTokenError:
        return {}