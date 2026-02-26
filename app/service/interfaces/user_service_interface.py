from abc import ABC, abstractmethod
from app.schema.user import CreateUserInput, User


class IUserService(ABC):
    @abstractmethod
    def create_user(self, user: CreateUserInput) -> User:
        pass

    @abstractmethod
    async def get_by_email(self, email: str) -> User:
        pass
