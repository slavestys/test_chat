from typing import Annotated

from fastapi import Depends

from .services import MessageService, MessageSearchService


message_service_dependency = Annotated[MessageService, Depends()]
message_search_service_dependency = Annotated[MessageSearchService, Depends()]
