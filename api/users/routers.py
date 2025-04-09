from fastapi import APIRouter

from . import dependensies
from .schemas import UserGetSchema, TokenSchema, UserSearchSchema

router = APIRouter()


@router.post("/sign_up/", response_model=UserGetSchema)
async def sign_up(service: dependensies.registration_service_dependency):
    """
    User register

    Register user
    """
    return await service.process()


@router.post("/get_token/", response_model=TokenSchema)
async def get_authorization_token(service: dependensies.get_token_service_dependency):
    """
    Authorization token get

    Get authorization token
    """
    return await service.process()


@router.get("/search/", response_model=list[UserGetSchema])
async def search(service: dependensies.search_service_dependency):
    """
    Authorization token get

    Get authorization token
    """
    return await service.process()

