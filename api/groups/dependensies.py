from typing import Annotated

from fastapi import Depends

from .services import GroupCreateService, GroupsListService, GroupJoinService


group_create_service_dependency = Annotated[GroupCreateService, Depends()]
groups_list_service_dependency = Annotated[GroupsListService, Depends()]
group_join_service_dependency = Annotated[GroupJoinService, Depends()]
