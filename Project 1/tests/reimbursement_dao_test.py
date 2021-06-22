from typing import List
from unittest import TestCase
from entities.user import User
from entities.reimbursement import Reimbursement
from daos.user_dao_base import UserDAOBase
from daos.user_dao_postgres import UserDAOPostgres
from daos.reimbursement_dao_base import ReimbursementDAOBase
from daos.reimbursement_dao_postgres import ReimbursementDAOPostgres
from exceptions.invalid_param_exception import InvalidParamError
from exceptions.not_found_exception import ResourceNotFoundError

user_dao: UserDAOBase = UserDAOPostgres()
employee1: User = User("Test", "test", "password")
employee2: User = User("Test2", "test2", "password")


reim_dao: ReimbursementDAOBase = ReimbursementDAOPostgres()
reim1: Reimbursement = Reimbursement(500, "Need help", "Sure")
reim2: Reimbursement = Reimbursement(1000, "Also need help", "Sure")


def test_post_reimbursement():
    user_dao.post_user(employee1)
    user_dao.post_user(employee2)
    assert reim_dao.post_reimbursement(employee1.get_id(), reim1)
    assert reim_dao.post_reimbursement(employee2.get_id(), reim2)


def test_post_reimbursement_invalid():
    try:
        reim_dao.post_reimbursement(employee1.get_id(), reim1)
        assert False
    except InvalidParamError:
        assert True


def test_remove_reimbursement_fail():
    try:
        reim_dao.remove_reimbursement(-1)
        assert False
    except ResourceNotFoundError:
        assert True


def test_get_reimbursement_by_id_fail():
    try:
        reim_dao.get_reimbursement_by_id(-1)
        assert False
    except ResourceNotFoundError:
        assert True


def test_get_reimbursement_by_id():
    temp_rein: Reimbursement = reim_dao.get_reimbursement_by_id(reim1.get_id())
    TestCase().assertDictEqual(temp_rein.to_json_dict(), reim1.to_json_dict())


def test_get_user_pending_reimbursement_fail():
    try:
        reim_dao.get_user_pending_reimbursement(-1)
        assert False
    except ResourceNotFoundError:
        assert True


def test_get_user_pending_reimbursement():
    temp_rein: Reimbursement = reim_dao.get_user_pending_reimbursement(employee1.get_id())
    TestCase().assertDictEqual(temp_rein.to_json_dict(), reim1.to_json_dict())


def test_get_all_reimbursement():
    rein_list: List[Reimbursement] = reim_dao.get_all_reimbursement()
    assert len(rein_list) > 0
    # TestCase().assertDictEqual(rein_list[0].to_json_dict(), reim1.to_json_dict())
    # TestCase().assertDictEqual(rein_list[1].to_json_dict(), reim2.to_json_dict())


def test_get_all_user_reimbursement():
    rein_list: List[Reimbursement] = reim_dao.get_all_user_reimbursement(employee1.get_id())
    assert len(rein_list) == 1
    TestCase().assertDictEqual(rein_list[0].to_json_dict(), reim1.to_json_dict())


def test_get_all_pending_reimbursement1():
    rein_list: List[Reimbursement] = reim_dao.get_all_pending_reimbursement()
    TestCase().assertDictEqual(rein_list[0].to_json_dict(), reim1.to_json_dict())
    TestCase().assertDictEqual(rein_list[1].to_json_dict(), reim2.to_json_dict())


def test_update_user_reimbursement_fail():
    try:
        reim_dao.update_user_reimbursement(-1, reim1)
        assert False
    except ResourceNotFoundError:
        assert True


def test_update_user_reimbursement_pass():
    # Employees can only update amounts and reasons
    temp_reim: Reimbursement = Reimbursement(1000, "Accident", "Wow, you really need help")
    temp_reim.set_status(2, 1)
    reim_dao.update_user_reimbursement(employee1.get_id(), temp_reim)
    updated_reim = reim_dao.get_reimbursement_by_id(temp_reim.get_id())
    assert updated_reim.get_id() == reim1.get_id()
    assert updated_reim.get_status() == reim1.get_status()
    assert updated_reim.get_owner_id() == reim1.get_owner_id()
    assert updated_reim.get_amount() == temp_reim.get_amount()
    assert updated_reim.get_reason() == temp_reim.get_reason()
    assert not updated_reim.get_response() == temp_reim.get_response()


def test_update_reimbursement_pass():
    # Managers can only update status and response
    temp_reim: Reimbursement = Reimbursement(2000, "Different", "Ok, I guess...")
    temp_reim.set_status(2, 1)
    reim_dao.update_reimbursement(reim1.get_id(), temp_reim)
    updated_reim = reim_dao.get_reimbursement_by_id(temp_reim.get_id())
    assert updated_reim.is_approved()
    assert updated_reim.get_id() == reim1.get_id()
    assert updated_reim.get_owner_id() == reim1.get_owner_id()
    assert updated_reim.get_response() == temp_reim.get_response()
    assert not updated_reim.get_reason() == temp_reim.get_reason()
    assert not updated_reim.get_amount() == temp_reim.get_amount()


def test_update_reimbursement_fail():
    try:
        reim_dao.update_reimbursement(-1, reim1)
        assert False
    except ResourceNotFoundError:
        assert True


def test_get_user_pending_reimbursement_invalid():
    # Previous reimbursement was approved
    try:
        reim_dao.get_user_pending_reimbursement(employee1.get_id())
        assert False
    except ResourceNotFoundError:
        assert True


def test_remove_reimbursement():
    # Doubles as clean up
    assert reim_dao.remove_reimbursement(reim1.get_id())
    assert reim_dao.remove_reimbursement(reim2.get_id())
    user_dao.remove_user(employee1.get_id())
    user_dao.remove_user(employee2.get_id())
