from app.service.interfaces.user_service_interface import IUserService
from app.schema.user import CreateUserInput, UserOutput
from app.service.security.hasher import HashingService
from app.model.user import UserORM


class RegisterUser:
    def __init__(self, user_service: IUserService) -> None:
        self._user_service = user_service

    async def execute(self, input: CreateUserInput) -> UserOutput:

        existing = await self._user_service.get_by_email(input.email)
        if existing:
            raise ValueError("Email already registered")

        if not isinstance(input.hashed_password, str):
            raise TypeError("Password must be a string")
        if not isinstance(input.email, str):
            raise TypeError("Email must be a string")

        hashed_password = HashingService.get_hashed_password(input.hashed_password)
        input.hashed_password = hashed_password

        domain_user = UserORM(**input.model_dump())

        orm_user = await self._user_service.create_user(domain_user)
        if orm_user is None:
            raise RuntimeError("Failed to create user: ORM returned None")
        return UserOutput.model_validate(orm_user)
