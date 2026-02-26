from app.service.interfaces.user_service_interface import IUserService
from app.schema.user import CreateUserInput


class CreateUser:
    def __init__(self, user_service: IUserService) -> None:
        self._user_service = user_service

    async def execute(self, user: CreateUserInput):

        async with self._user_service._session.begin():
            existing = await self._user_service.get_by_email(user.email)
            if existing:
                raise ValueError("Email already registered")
            saved = await self._user_service.create_user(user=user)
        await self._user_service._session.refresh(saved)
        return saved
