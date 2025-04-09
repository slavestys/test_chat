from typing import Annotated

from fastapi import Depends

from .services import RegistrationService, GetTokenService, SearchService


registration_service_dependency = Annotated[RegistrationService, Depends()]
get_token_service_dependency = Annotated[GetTokenService, Depends()]
search_service_dependency = Annotated[SearchService, Depends()]
