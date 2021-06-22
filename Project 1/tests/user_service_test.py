from unittest.mock import MagicMock
from services.user_service import UserService
from services.login_manager import login_manager
from daos.user_dao_base import UserDAOBase
from daos.user_dao_postgres import UserDAOPostgres
from entities.user import User
from exceptions.access_exception import AccessError

employee: User = User("Test", "test", "password")
manager: User = User("Test2", "test2", "password")
manager.set_role(2, 2)
manager.clear_role(2, 1)
mock_dao: UserDAOBase = UserDAOPostgres()

# Mocked methods
mock_dao.post_user_as_manager = MagicMock(return_value=True)
mock_dao.post_user = MagicMock(return_value=True)


def mock_get_user_by_credentials(username: str, password: str):
    if username == employee.get_username():
        return employee
    elif username == manager.get_username():
        return manager


mock_dao.get_user_by_credentials = MagicMock(side_effect=mock_get_user_by_credentials)


def mock_get_user_by_id(user_id: int):
    if user_id == employee.get_id():
        return employee
    elif user_id == manager.get_id():
        return manager


mock_dao.get_user_by_id = MagicMock(side_effect=mock_get_user_by_id)


def mock_update_user_as_employee(user_id: int, user: User):
    # User should have no role flags if called
    user.clear_role(2, 3)
    return True


mock_dao.update_user_as_employee = MagicMock(side_effect=mock_update_user_as_employee)


def mock_update_user_as_manager(user_id: int, user: User):
    # User should now be an employee if called
    user.clear_role(2, 2)
    user.set_role(2, 1)
    return True


mock_dao.update_user_as_manager = MagicMock(side_effect=mock_update_user_as_manager)
mock_dao.remove_user = MagicMock(return_value=True)
user_service: UserService = UserService(mock_dao)


def test_login():
    result: User = user_service.login(manager.get_username(), manager.get_password())
    assert result == manager
    assert login_manager.get_user_role(manager.get_username()) == manager.get_role()


def test_already_login():
    try:
        result: User = user_service.login(manager.get_username(), manager.get_password())
        assert False
    except AccessError:
        assert True


def test_post_user_no_username():
    assert user_service.post_user("", employee)
    assert login_manager.get_user_role(employee.get_username()) == employee.get_role()


def test_post_user_as_employee():
    try:
        user_service.post_user(employee.get_username(), employee)
        assert False
    except AccessError:
        assert True


def test_post_user_as_manager():
    employee2: User = User("NA", "na", "password")
    assert user_service.post_user(manager.get_username(), employee2)
    # New user should not be logged in
    try:
        login_manager.get_user_role(employee2.get_username())
        assert False
    except AccessError:
        assert True


def test_get_user_as_no_username():
    try:
        user_service.get_user("", employee.get_id())
        assert False
    except AccessError:
        assert True


def test_get_user_as_employee():
    try:
        user_service.get_user(employee.get_username(), employee.get_id())
        assert False
    except AccessError:
        assert True


def test_get_user_as_manager():
    result: User = user_service.get_user(manager.get_username(), employee.get_id())
    assert result == employee


def test_update_user_as_no_username():
    try:
        user_service.update_user("", employee.get_id(), employee)
        assert False
    except AccessError:
        assert True


def test_update_user_as_employee():
    user_service.update_user(employee.get_username(), employee.get_id(), employee)
    assert employee.get_role() == 0


def test_update_user_as_manager():
    user_service.update_user(manager.get_username(), employee.get_id(), employee)
    assert employee.get_role() == 1


def test_remove_user_as_no_username():
    try:
        user_service.remove_user("", employee.get_id())
        assert False
    except AccessError:
        assert True


def test_remove_user_as_employee():
    try:
        user_service.remove_user(employee.get_username(), employee.get_id())
        assert False
    except AccessError:
        assert True


def test_remove_user_as_manager():
    assert user_service.remove_user(manager.get_username(), employee.get_id())


def test_logout():
    # Ensure users are actually logged out
    assert user_service.logout(employee.get_username())
    try:
        login_manager.get_user_role(employee.get_username())
        assert False
    except AccessError:
        assert True

    assert user_service.logout(manager.get_username())
    try:
        login_manager.get_user_role(manager.get_username())
        assert False
    except AccessError:
        assert True
