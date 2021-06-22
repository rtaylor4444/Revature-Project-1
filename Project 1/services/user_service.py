from services.user_service_base import UserServiceBase
from entities.user import User
from daos.user_dao_base import UserDAOBase
from services.login_manager import login_manager
from exceptions.access_exception import AccessError


class UserService(UserServiceBase):

    def __init__(self, user_dao: UserDAOBase):
        self.__user_dao = user_dao

    def post_user(self, username: str, user: User) -> bool:
        try:
            incoming_role: int = login_manager.get_user_role(username)
            if incoming_role & 2 != 0:
                self.__user_dao.post_user_as_manager(user)
                return True
            else:
                raise AccessError("Access Denied")
        except AccessError:
            self.__user_dao.post_user(user)

        self.login(user.get_username(), user.get_password())
        return True

    def login(self, username: str, password: str) -> User:
        user: User = self.__user_dao.get_user_by_credentials(username, password)
        login_manager.login(user.get_username(), user)
        return user

    def logout(self, username: str) -> bool:
        login_manager.logout(username)
        return True

    def get_user(self, username: str, user_id: int) -> User:
        if login_manager.get_user_role(username) & 2 != 0:
            return self.__user_dao.get_user_by_id(user_id)
        else:
            raise AccessError("Access Denied")

    def update_user(self, username: str, user_id: int, user: User) -> bool:
        if login_manager.get_user_role(username) & 2 != 0:
            return self.__user_dao.update_user_as_manager(user_id, user)
        else:
            return self.__user_dao.update_user_as_employee(login_manager.get_user_id(username), user)

    def remove_user(self, username: str, user_id: int) -> bool:
        if login_manager.get_user_role(username) & 2 != 0:
            return self.__user_dao.remove_user(user_id)
        else:
            raise AccessError("Access Denied")
