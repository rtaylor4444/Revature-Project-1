from abc import ABC, abstractmethod
from entities.user import User


class UserServiceBase(ABC):

    @abstractmethod
    def post_user(self, username: str, user: User) -> bool:
        pass

    @abstractmethod
    def login(self, username: str, password: str) -> User:
        pass

    @abstractmethod
    def logout(self, username: str) -> bool:
        pass

    @abstractmethod
    def get_user(self, username: str, user_id: int) -> User:
        pass

    @abstractmethod
    def update_user(self, incoming_role: int, user_id: int, user: User) -> bool:
        pass

    @abstractmethod
    def remove_user(self, username: str, user_id: int) -> bool:
        pass
