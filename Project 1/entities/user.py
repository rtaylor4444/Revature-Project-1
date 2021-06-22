from exceptions.invalid_param_exception import InvalidParamError


class User:

    def __init__(self, name: str = "", username: str = "", password: str = "", role: int = 1):
        self.__id = 0
        self.__name = name
        self.__username = username
        self.__password = password
        self.__is_blackmark = False
        # Roles 1 = employee, 2 = manager, 3 = both
        self.__role = role

    def get_name(self) -> str:
        return self.__name

    def get_username(self) -> str:
        return self.__username

    def get_password(self) -> str:
        return self.__password

    def get_role(self) -> int:
        return self.__role

    def is_blackmarked(self) -> bool:
        return self.__is_blackmark

    def is_manager(self) -> bool:
        return bool(self.__role & 2)

    def is_employee(self) -> bool:
        return bool(self.__role & 1)

    def get_id(self) -> int:
        return self.__id

    def set_id(self, new_id: int) -> bool:
        if self.__id != 0:
            return False

        self.__id = new_id
        return True

    def set_blackmark(self, incoming_role: int, blackmark: bool) -> bool:
        # Only managers can add/remove blackmarks
        if incoming_role & 2 == 0:
            return False

        self.__is_blackmark = blackmark
        return True

    def set_role(self, incoming_role: int, new_role: int) -> bool:
        # Only managers can set new managers
        if incoming_role & 2 == 0:
            return False
        if new_role < 1 or new_role > 3:
            raise InvalidParamError("invalid role flag")

        self.__role |= new_role
        return True

    def clear_role(self, incoming_role: int, new_role: int):
        # Only managers can set new managers
        if incoming_role & 2 == 0:
            return False
        if new_role < 1 or new_role > 3:
            raise InvalidParamError("invalid role flag")

        self.__role &= ~new_role

    def to_json_dict(self):
        return {
            "id": self.__id,
            "name": self.__name,
            "username": self.__username,
            "password": self.__password,
            "blackmark": self.__is_blackmark,
            "role": self.__role
        }

    def set_from_json(self, incoming_role: int, json: dict):
        name = str(json.get("name"))
        if json.get("name") is None:
            raise InvalidParamError("name param missing")
        elif len(name) < 3 or len(name) > 50:
            raise InvalidParamError("name must be between 3 and 50 characters")

        username = str(json.get("username"))
        if json.get("username") is None:
            raise InvalidParamError("username param missing")
        elif len(username) < 3 or len(username) > 50:
            raise InvalidParamError("username must be between 3 and 50 characters")

        password = str(json.get("password"))
        if json.get("password") is None:
            raise InvalidParamError("password param missing")
        elif len(password) < 3 or len(password) > 50:
            raise InvalidParamError("password must be between 3 and 50 characters")

        # Managers must pass in the below two fields
        if incoming_role == 2:
            new_role = json.get("role")
            if new_role is None:
                raise InvalidParamError("role param missing")
            elif str(new_role).isdigit():
                self.set_role(incoming_role, int(new_role))

            blackmark = json.get("blackmark")
            if blackmark is None:
                raise InvalidParamError("blackmark param missing")
            elif isinstance(blackmark, bool):
                self.set_blackmark(incoming_role, bool(blackmark))

        self.__name = name
        self.__username = username
        self.__password = password
