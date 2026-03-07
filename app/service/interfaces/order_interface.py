from abc import ABC, abstractmethod


class IOder(ABC):
    @abstractmethod
    def place_order():
        pass

    @abstractmethod
    def get_order():
        pass
