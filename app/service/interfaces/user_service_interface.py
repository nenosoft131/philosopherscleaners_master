from abc import ABC, abstractmethod
from app.schema.user import CreateUserInput
from app.model.user import UserORM


class IUserService(ABC):
    @abstractmethod
    def create_user(self, user: UserORM) -> UserORM:
        pass

    @abstractmethod
    async def get_by_email(self, email: str) -> UserORM:
        pass
