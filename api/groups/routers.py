from fastapi import APIRouter

from . import dependensies
from . import schemas

router = APIRouter()


@router.post("/create/", response_model=schemas.GroupGetSchema)
async def group_create(service: dependensies.group_create_service_dependency):
    """
    Group create

    Create group by params
    """
    return await service.process()


@router.get("/list/", response_model=list[schemas.GroupGetSchema])
async def groups_list(service: dependensies.groups_list_service_dependency):
    """
    Groups list

    search groups
    """
    return await service.process()


@router.put("/{group_id}/join/", response_model=schemas.GroupGetSchema)
async def group_join(service: dependensies.group_join_service_dependency):
    """
    Groups list

    search groups
    """
    return await service.process()