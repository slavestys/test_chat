import os
from datetime import timedelta


TOKEN_SECRET_KEY = os.getenv("SECRET_KEY", "replace")
TOKEN_ALGORITHM = "HS256"
TOKEN_EXPIRATION = timedelta(hours=1)