from fastapi import APIRouter

from . import dependensies
from .schemas import MessageSchema

router = APIRouter()


@router.post("/send/", response_model=MessageSchema)
async def send_message(message_service: dependensies.message_service_dependency):
    """
    Sand message

    Send message to chat
    """
    return await message_service.process()


@router.get("/list/", response_model=list[MessageSchema])
async def search(service: dependensies.message_search_service_dependency):
    """
    Messages list

    Get list of messages
    """
    return await service.process()
