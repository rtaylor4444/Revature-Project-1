from daos.user_dao_base import UserDAOBase
from entities.user import User
from utils.connection_util import connection
from exceptions.invalid_param_exception import InvalidParamError
from exceptions.not_found_exception import ResourceNotFoundError


class UserDAOPostgres(UserDAOBase):

    def __init__(self) -> None:
        pass

    def verify_username(self, user: User) -> bool:
        # Check if this username already exists
        sql = """select * from re_user where username = %s"""
        cursor = connection.cursor()
        cursor.execute(sql, (user.get_username(),))
        result = cursor.fetchone()
        if result is not None:
            raise InvalidParamError("Invalid username, pick another")
        return True

    def post_user(self, user: User) -> bool:
        user.set_role(2, 1)
        user.set_blackmark(2, False)
        return self.post_user_as_manager(user)

    def post_user_as_manager(self, user: User) -> bool:
        self.verify_username(user)

        # Add new user to the database
        sql = """insert into re_user (firstname, username, user_password, blackmark, user_role) 
                values (%s,%s,%s,%s,%s) returning user_id"""
        cursor = connection.cursor()
        cursor.execute(sql, (user.get_name(), user.get_username(), user.get_password(),
                             user.is_blackmarked(), user.get_role()))
        connection.commit()
        result = cursor.fetchone()
        if result is None:
            raise ResourceNotFoundError("User with this id does not exist")

        user.set_id(result[0])
        return True

    def get_user_by_id(self, user_id: int) -> User:
        sql = """select * from re_user where user_id = %s"""
        cursor = connection.cursor()
        cursor.execute(sql, [user_id])
        record = cursor.fetchone()
        if record is None:
            raise ResourceNotFoundError("User with this id does not exist")

        user = User(record[1], record[2], record[3], record[5])
        user.set_id(record[0])
        user.set_blackmark(2, record[4])
        return user

    def get_user_by_credentials(self, username: str, password: str) -> User:
        sql = """select * from re_user where username = %s and user_password = %s"""
        cursor = connection.cursor()
        cursor.execute(sql, [username, password])
        record = cursor.fetchone()
        if record is None:
            raise ResourceNotFoundError("Invalid username or password")

        user = User(record[1], record[2], record[3], record[5])
        user.set_id(record[0])
        user.set_blackmark(2, record[4])
        return user

    def __update_user(self, user_id: int, user: User) -> bool:
        # Update user in the database
        sql = """update re_user set firstname=%s, username=%s, user_password=%s, blackmark=%s, 
        user_role=%s where user_id =%s returning user_id"""
        cursor = connection.cursor()
        cursor.execute(sql, [user.get_name(), user.get_username(), user.get_password(),
                             user.is_blackmarked(), user.get_role(), user_id])
        connection.commit()
        record = cursor.fetchone()
        if record is None:
            raise ResourceNotFoundError("User with this id does not exist")

        user.set_id(user_id)
        return True

    def update_user_as_employee(self, user_id: int, user: User) -> bool:
        cur_user: User = self.get_user_by_id(user_id)

        # If updating username it must not exist
        if cur_user.get_username() != user.get_username():
            self.verify_username(user)

        # Set uneditable fields
        user.set_blackmark(2, cur_user.is_blackmarked())
        user.clear_role(2, 3)
        user.set_role(2, cur_user.get_role())
        return self.__update_user(user_id, user)

    def update_user_as_manager(self, user_id: int, user: User) -> bool:
        # If updating username it must not exist
        cur_user: User = self.get_user_by_id(user_id)
        if cur_user.get_username() != user.get_username():
            self.verify_username(user)

        return self.__update_user(user_id, user)

    def remove_user(self, user_id: int) -> bool:
        sql = """delete from re_user where user_id =%s returning user_id"""
        cursor = connection.cursor()
        cursor.execute(sql, [user_id])
        connection.commit()
        record = cursor.fetchone()
        if record is None:
            raise ResourceNotFoundError("User with this id does not exist")

        return True
