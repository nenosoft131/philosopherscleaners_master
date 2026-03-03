from app.service.interfaces.user_service_interface import IUserService
from app.schema.user import CreateUserInput, UserOutput
from app.service.security.hasher import HashingService
from sqlalchemy.exc import IntegrityError
from app.model.user import UserORM


class RegisterUser:
    def __init__(self, user_service: IUserService) -> None:
        self._user_service = user_service

    async def execute(self, input: CreateUserInput) -> UserOutput:

        existing = await self._user_service.get_by_email(input.email)
        if existing:
            raise ValueError("Email already registered")

        if not isinstance(input.hash_password, str):
            raise TypeError("Password must be a string")
        if not isinstance(input.email, str):
            raise TypeError("Email must be a string")

        hashed_password = HashingService.get_hashed_password(input.hash_password)

        domain_user = UserORM(
            first_name=input.first_name,
            last_name=input.last_name,
            email=input.email,
            hashed_password=hashed_password,
            role=input.user_role,
            is_active=input.is_active,
        )

        orm_user = await self._user_service.create_user(domain_user)
        if orm_user is None:
            raise RuntimeError("Failed to create user: ORM returned None")
        return UserOutput(
            id=orm_user.id,
            email=orm_user.email,
            first_name=orm_user.first_name,
            last_name=orm_user.last_name,
            user_role=orm_user.role,
            is_active=orm_user.is_active,
        )
