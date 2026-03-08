from abc import ABC, abstractmethod


class IPasswordHasher(ABC):
    @abstractmethod
    def get_hashed_password(password: str) -> str:
        pass

    @abstractmethod
    def validate_password(hashed_password: str, plain_password: str):
        pass
