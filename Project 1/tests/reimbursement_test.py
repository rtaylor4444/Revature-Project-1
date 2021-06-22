from unittest import TestCase
from entities.reimbursement import Reimbursement
from exceptions.invalid_param_exception import InvalidParamError

reimburse: Reimbursement = Reimbursement(500, "Need help", "Sure")
reimburse_second: Reimbursement = Reimbursement(1000, "Also need help", "Sure")


def test_get_amount():
    assert reimburse.get_amount() == 500


def test_get_reason():
    assert reimburse.get_reason() == "Need help"


def test_get_response():
    assert reimburse.get_response() == "Sure"


def test_get_id():
    assert reimburse.get_id() == 0


def test_get_owner_id():
    assert reimburse.get_owner_id() == 0


def test_get_status():
    assert reimburse.get_status() == 0


def test_set_id():
    reimburse.set_id(1)
    assert reimburse.get_id() == 1
    reimburse.set_id(2)
    assert reimburse.get_id() == 1


def test_set_owner_id():
    reimburse.set_owner_id(1)
    assert reimburse.get_id() == 1
    reimburse.set_owner_id(2)
    assert reimburse.get_id() == 1


def test_set_status():
    reimburse.set_status(1, -1)
    assert not reimburse.is_denied()
    assert reimburse.is_pending()
    reimburse.set_status(2, 1)
    assert not reimburse.is_pending()
    assert reimburse.is_approved()
    reimburse.set_status(2, -1)
    assert reimburse.is_approved()


def test_set_response():
    reimburse.set_response(1, "I refuse")
    assert not reimburse.get_response() == "I refuse"
    reimburse.set_response(2, "Sure you need it")
    assert reimburse.get_response() == "Sure you need it"


def test_to_json_dict():
    new_json = {
        "id": 1,
        "amount": 500,
        "reason": "Need help",
        "owner": 1,
        "status": 1,
        "response": "Sure you need it"
    }
    TestCase().assertDictEqual(new_json, reimburse.to_json_dict())


def test_set_from_json_fail():
    # Missing amount
    new_json = {
        "reason": "Need help",
        "owner": 1
    }
    try:
        reimburse.set_from_json(1, new_json)
        assert False
    except InvalidParamError:
        assert True

    # Missing reason
    new_json = {
        "amount": 1000,
        "owner": 1
    }
    try:
        reimburse.set_from_json(1, new_json)
        assert False
    except InvalidParamError:
        assert True

    # Missing owner id
    new_json = {
        "reason": "Need help",
        "amount": 1000
    }
    try:
        reimburse.set_from_json(1, new_json)
        assert False
    except InvalidParamError:
        assert True


def test_set_from_json_invalid():
    # Invalid amount
    new_json = {
        "amount": "a letter",
        "reason": "Need help",
        "owner": 1
    }
    try:
        reimburse.set_from_json(1, new_json)
        assert False
    except InvalidParamError:
        assert True

    # Invalid owner
    new_json = {
        "amount": 1000,
        "reason": "Need help",
        "owner": "a letter"
    }
    try:
        reimburse.set_from_json(1, new_json)
        assert False
    except InvalidParamError:
        assert True


def test_set_from_json_invalid_status():
    new_json = {
        "amount": 1000,
        "reason": "Need help",
        "owner": 1,
        "status": "a letter"
    }
    try:
        reimburse_second.set_from_json(2, new_json)
        assert False
    except InvalidParamError:
        assert True

    new_json = {
        "amount": 1000,
        "reason": "Need help",
        "owner": 1,
        "status": 200000000
    }
    try:
        reimburse_second.set_from_json(2, new_json)
        assert False
    except InvalidParamError:
        assert True


def test_set_from_json_pass():
    new_json = {
        "amount": 100,
        "reason": "Need help*",
        "owner": 3,
        "status": 1,
        "response": "Sure"
    }
    reimburse_second.set_from_json(2, new_json)
    assert reimburse_second.get_amount() == new_json["amount"]
    assert reimburse_second.is_approved()
    assert reimburse_second.get_reason() == new_json["reason"]
    assert reimburse_second.get_response() == new_json["response"]
    assert reimburse_second.get_owner_id() == new_json["owner"]
