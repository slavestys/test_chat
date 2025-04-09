from http import HTTPStatus

from fastapi.exceptions import HTTPException

from db.seevice import BaseDBService
from db.dependencies import session_dependency

from ..schemas import RegistrationSchema
from ..password import get_password_hash
from ..repository import users_repository


class RegistrationService(BaseDBService):
    registration: RegistrationSchema
    users: users_repository

    def __init__(self, registration: RegistrationSchema, session: session_dependency, users: users_repository):
        super(RegistrationService, self).__init__(session)
        self.registration = registration
        self.users = users

    async def process(self):
        user = await self.users.find_by_email(self.registration.email)
        if user:
            raise HTTPException(
                status_code=HTTPStatus.UNPROCESSABLE_ENTITY,
                detail={"type": "not-unique", "loc": ["email"]}
            )
        return await self.users.create(
            name=self.registration.name,
            email=self.registration.email,
            password=get_password_hash(self.registration.password)
        )