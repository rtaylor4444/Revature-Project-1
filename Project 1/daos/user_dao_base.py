from abc import ABC, abstractmethod
from entities.user import User


class UserDAOBase(ABC):

    @abstractmethod
    def __init__(self) -> None:
        pass

    @abstractmethod
    def verify_username(self, user: User) -> bool:
        pass

    @abstractmethod
    def post_user(self, user: User) -> bool:
        pass

    @abstractmethod
    def post_user_as_manager(self, user: User) -> bool:
        pass

    @abstractmethod
    def get_user_by_id(self, user_id: int) -> User:
        pass

    @abstractmethod
    def get_user_by_credentials(self, username: str, password: str) -> User:
        pass

    @abstractmethod
    def update_user_as_employee(self, user_id: int, user: User) -> bool:
        pass

    @abstractmethod
    def update_user_as_manager(self, user_id: int, user: User) -> bool:
        pass

    @abstractmethod
    def remove_user(self, user_id: int) -> bool:
        pass
