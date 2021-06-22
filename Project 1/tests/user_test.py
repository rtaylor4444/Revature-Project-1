from unittest import TestCase
from entities.user import User
from exceptions.invalid_param_exception import InvalidParamError

employee: User = User("John", "employee", "password", 1)
manager: User = User("Chris", "manager", "password123", 2)
promoted: User = User("Rob", "promoted", "secure456", 3)


def test_get_name():
    assert employee.get_name() == "John"


def test_get_username():
    assert employee.get_username() == "employee"


def test_get_password():
    assert employee.get_password() == "password"


def test_get_role():
    assert employee.get_role() == 1


def test_is_blackmarked():
    assert not employee.is_blackmarked()


def test_is_manager():
    assert not employee.is_manager()
    assert manager.is_manager()
    assert promoted.is_manager()


def test_is_employee():
    assert employee.is_employee()
    assert promoted.is_employee()
    assert not manager.is_employee()


def test_get_id():
    assert employee.get_id() == 0


def test_set_id():
    employee.set_id(1)
    assert employee.get_id() == 1
    employee.set_id(2)
    assert employee.get_id() == 1


def test_set_blackmark():
    employee.set_blackmark(1, True)
    assert not employee.is_blackmarked()
    employee.set_blackmark(2, True)
    assert employee.is_blackmarked()
    employee.set_blackmark(3, False)
    assert not employee.is_blackmarked()


def test_set_role():
    employee.set_role(1, 2)
    assert employee.get_role() == 1
    employee.set_role(2, 2)
    assert employee.get_role() == 3
    try:
        employee.set_role(2, -4)
        assert False
    except InvalidParamError:
        assert True


def test_clear_role():
    employee.clear_role(1, 2)
    assert employee.get_role() == 3
    employee.clear_role(2, 2)
    assert employee.get_role() == 1
    try:
        employee.clear_role(2, -4)
        assert False
    except InvalidParamError:
        assert True


def test_to_json_dict():
    TestCase().assertDictEqual({
        "id": 1,
        "name": "John",
        "username": "employee",
        "password": "password",
        "blackmark": False,
        "role": 1
        }, employee.to_json_dict())


def test_set_from_json_fail():
    # Missing name
    new_json = {
        "username": "employee",
        "password": "password",
        "blackmark": False,
        "role": 1
    }
    try:
        employee.set_from_json(2, new_json)
        assert False
    except InvalidParamError:
        assert True

    # Missing username
    new_json = {
        "name": "Jane",
        "password": "password",
        "blackmark": False,
        "role": 1
    }
    try:
        employee.set_from_json(2, new_json)
        assert False
    except InvalidParamError:
        assert True

    # Missing password
    new_json = {
        "name": "Jane",
        "username": "employee",
        "blackmark": False,
        "role": 1
    }
    try:
        employee.set_from_json(2, new_json)
        assert False
    except InvalidParamError:
        assert True


def test_set_from_json_access_pass():
    new_json = {
        "name": "Jane",
        "username": "employee",
        "password": "password"
    }
    employee.set_from_json(1, new_json)
    assert employee.get_name() == new_json["name"]
    assert employee.get_username() == new_json["username"]
    assert employee.get_password() == new_json["password"]


def test_set_from_json_access_fail():
    new_json = {
        "name": "Jane",
        "username": "employee",
        "password": "password",
        "blackmark": True,
        "role": 3
    }
    employee.set_from_json(1, new_json)
    assert employee.get_name() == new_json["name"]
    assert employee.get_username() == new_json["username"]
    assert employee.get_password() == new_json["password"]
    assert employee.is_blackmarked() != new_json["blackmark"]
    assert employee.get_role() != new_json["role"]


def test_set_from_json_access_invalid1():
    # Invalid name
    new_json = {
        "name": "",
        "username": "employee",
        "password": "password",
        "blackmark": True,
        "role": 3
    }
    try:
        employee.set_from_json(2, new_json)
    except InvalidParamError:
        assert True

    # Invalid username
    new_json = {
        "name": "Jane",
        "username": "",
        "password": "password",
        "blackmark": True,
        "role": 3
    }
    try:
        employee.set_from_json(2, new_json)
    except InvalidParamError:
        assert True

    # Invalid password
    new_json = {
        "name": "Jane",
        "username": "employee",
        "password": "",
        "blackmark": True,
        "role": 3
    }
    try:
        employee.set_from_json(2, new_json)
    except InvalidParamError:
        assert True


def test_set_from_json_access_invalid2():
    new_json = {
        "name": 123,
        "username": 123,
        "password": 123,
        "blackmark": "a letter",
        "role": "a letter"
    }
    employee.set_from_json(2, new_json)
    assert employee.get_name() == str(new_json["name"])
    assert employee.get_username() == str(new_json["username"])
    assert employee.get_password() == str(new_json["password"])
    assert not employee.is_blackmarked()
    assert employee.get_role() != new_json["role"]


def test_set_from_json_access_missing_param1():
    new_json = {
        "name": "Jane",
        "username": "employee",
        "password": "password",
        "role": 1
    }
    try:
        employee.set_from_json(2, new_json)
        assert False
    except InvalidParamError:
        assert True


def test_set_from_json_access_missing_param2():
    new_json = {
        "name": "Jane",
        "username": "employee",
        "password": "password",
        "blackmark": True
    }
    try:
        employee.set_from_json(2, new_json)
        assert False
    except InvalidParamError:
        assert True


def test_set_from_json_access_pass2():
    new_json = {
        "name": "Jane",
        "username": "employee",
        "password": "password",
        "blackmark": True,
        "role": 1
    }
    employee.set_from_json(2, new_json)
    assert employee.get_name() == new_json["name"]
    assert employee.get_username() == new_json["username"]
    assert employee.get_password() == new_json["password"]
    assert employee.is_blackmarked() == new_json["blackmark"]
    assert employee.is_employee()

