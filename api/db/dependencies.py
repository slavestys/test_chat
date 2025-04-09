from typing import Annotated

from fastapi import Depends

from .session import get_session


session_dependency = Annotated[get_session, Depends()]
