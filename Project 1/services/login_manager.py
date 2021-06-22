from entities.user import User
from exceptions.access_exception import AccessError
from exceptions.not_found_exception import ResourceNotFoundError


class LoginManager:

    def __init__(self):
        self.__logged_users = {}

    def login(self, username: str, incoming_user: User):
        if username in self.__logged_users:
            raise AccessError("This user is already logged in")

        self.__logged_users.update({username: {"role": incoming_user.get_role(),
                                               "id": incoming_user.get_id()}})

    def get_user_role(self, username: str):
        if username not in self.__logged_users:
            raise AccessError("This user is not logged in")

        return self.__logged_users[username]["role"]

    def get_user_id(self, username: str):
        if username not in self.__logged_users:
            raise AccessError("This user is not logged in")

        return self.__logged_users[username]["id"]

    def logout(self, username: str):
        if username in self.__logged_users:
            self.__logged_users.pop(username)


login_manager = LoginManager()
