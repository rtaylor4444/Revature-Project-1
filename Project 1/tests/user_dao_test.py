from unittest import TestCase
from entities.user import User
from daos.user_dao_base import UserDAOBase
from daos.user_dao_postgres import UserDAOPostgres
from exceptions.invalid_param_exception import InvalidParamError
from exceptions.not_found_exception import ResourceNotFoundError

user_dao: UserDAOBase = UserDAOPostgres()
employee: User = User("Test", "test", "password")
employee2: User = User("Test2", "test2", "password")


def test_post_user():
    assert user_dao.post_user(employee)


def test_post_user_fail():
    try:
        user_dao.post_user(employee)
        assert False
    except InvalidParamError:
        assert True


def test_post_user_as_manager():
    assert user_dao.post_user_as_manager(employee2)


def test_post_user_as_manager_fail():
    try:
        user_dao.post_user_as_manager(employee)
        assert False
    except InvalidParamError:
        assert True


def test_get_user_by_id():
    temp: User = user_dao.get_user_by_id(employee.get_id())
    TestCase().assertDictEqual(temp.to_json_dict(), employee.to_json_dict())


def test_get_user_by_id_fail():
    try:
        user_dao.get_user_by_id(-1)
        assert False
    except ResourceNotFoundError:
        assert True


def test_get_user_by_credentials():
    temp: User = user_dao.get_user_by_credentials(employee.get_username(), employee.get_password())
    TestCase().assertDictEqual(temp.to_json_dict(), employee.to_json_dict())


def test_get_user_by_credentials_fail():
    try:
        user_dao.get_user_by_credentials("", "")
        assert False
    except ResourceNotFoundError:
        assert True


def test_update_user_as_employee_fail():
    try:
        user_dao.update_user_as_employee(-1, employee)
        assert False
    except ResourceNotFoundError:
        assert True


def test_update_user_as_employee_invalid():
    # Taken username
    try:
        user_dao.update_user_as_employee(employee.get_id(), employee2)
        assert False
    except InvalidParamError:
        assert True


def test_update_user_as_manager_fail():
    try:
        user_dao.update_user_as_manager(-1, employee)
        assert False
    except ResourceNotFoundError:
        assert True


def test_update_user_as_manager_invalid():
    # Taken username
    try:
        user_dao.update_user_as_manager(employee.get_id(), employee2)
        assert False
    except InvalidParamError:
        assert True


def test_update_user_as_employee_pass():
    employee_update: User = User("Update", "update", "new_pass")
    employee_update.set_blackmark(2, True)
    employee_update.set_role(2, 2)
    assert user_dao.update_user_as_employee(employee.get_id(), employee_update)
    updated_user: User = user_dao.get_user_by_id(employee.get_id())
    assert updated_user.get_name() == employee_update.get_name()
    assert updated_user.get_username() == employee_update.get_username()
    assert updated_user.get_password() == employee_update.get_password()
    assert not updated_user.is_blackmarked()
    assert not updated_user.is_manager()


def test_update_user_as_manager_pass():
    employee_update: User = User("Update2", "update2", "new_pass")
    employee_update.set_blackmark(2, True)
    employee_update.set_role(2, 2)
    assert user_dao.update_user_as_manager(employee2.get_id(), employee_update)
    updated_user: User = user_dao.get_user_by_id(employee2.get_id())
    assert updated_user.get_name() == employee_update.get_name()
    assert updated_user.get_username() == employee_update.get_username()
    assert updated_user.get_password() == employee_update.get_password()
    assert updated_user.is_blackmarked()
    assert updated_user.is_manager()


def test_remove_user():
    # Doubles as cleanup
    assert user_dao.remove_user(employee.get_id())
    assert user_dao.remove_user(employee2.get_id())


def test_remove_user_fail():
    try:
        user_dao.remove_user(employee.get_id())
        assert False
    except ResourceNotFoundError:
        assert True


