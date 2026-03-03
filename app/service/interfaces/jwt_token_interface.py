from abc import ABC, abstractmethod


class ITokenGeneration(ABC):
    @abstractmethod
    def generate_token(self, data: dict) -> str:
        pass

    @abstractmethod
    def verify_token(self, token: str) -> dict:
        pass
