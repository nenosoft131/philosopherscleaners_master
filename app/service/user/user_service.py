from app.schema.user import CreateUserInput, User
from app.service.interfaces.user_service_interface import IUserService
from sqlalchemy.ext.asyncio import AsyncSession
from app.model.user import UserORM
from sqlalchemy.exc import IntegrityError
from sqlalchemy import select


class UserService(IUserService):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_by_email(self, email: str) -> UserORM:
        response = select(UserORM).where(UserORM.email == email)
        result = await self._session.execute(response)
        orm_user = result.scalar_one_or_none()
        return orm_user if orm_user else None

    async def create_user(self, orm_user: UserORM) -> UserORM:

        try:
            self._session.add(orm_user)
            await self._session.commit()
            await self._session.refresh(orm_user)
            return orm_user
        except IntegrityError:
            raise ValueError("Email already exist")
