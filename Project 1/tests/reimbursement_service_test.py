from unittest.mock import MagicMock
from services.reimbursement_service_base import ReimbursementServiceBase
from services.reimbursement_service import ReimbursementService
from services.login_manager import login_manager
from daos.reimbursement_dao_base import ReimbursementDAOBase
from daos.reimbursement_dao_postgres import ReimbursementDAOPostgres
from entities.user import User
from entities.reimbursement import Reimbursement
from exceptions.access_exception import AccessError

employee: User = User("Emp", "employee", "password")
manager: User = User("Man", "manager", "password")
manager.set_role(2, 2)
manager.clear_role(2, 1)
manager.set_id(1)

reim1: Reimbursement = Reimbursement(100, "Need help")
reim2: Reimbursement = Reimbursement(200, "Need help also")
login_manager.login(employee.get_username(), employee)
login_manager.login(manager.get_username(), manager)
mock_dao: ReimbursementDAOBase = ReimbursementDAOPostgres()

# Mocked Methods
mock_dao.post_reimbursement = MagicMock(return_value=True)


def mock_get_reimbursement_by_id(reim_id: int):
    if reim_id == 0:
        return reim1
    elif reim_id == 1:
        return reim2


mock_dao.get_reimbursement_by_id = MagicMock(side_effect=mock_get_reimbursement_by_id)
mock_dao.get_user_pending_reimbursement = MagicMock(return_value=True)
mock_dao.get_all_reimbursement = MagicMock(return_value=True)
mock_dao.get_all_user_reimbursement = MagicMock(return_value=True)
mock_dao.get_all_pending_reimbursement = MagicMock(return_value=True)


def mock_update_user_reimbursement(username: str, reim: Reimbursement):
    reim1.set_owner_id(1)


mock_dao.update_user_reimbursement = MagicMock(side_effect=mock_update_user_reimbursement)


def mock_update_reimbursement(reim_id: int, reim: Reimbursement):
    reim2.set_owner_id(2)


mock_dao.update_reimbursement = MagicMock(side_effect=mock_update_reimbursement)
mock_dao.remove_reimbursement = MagicMock(return_value=True)
reim_service: ReimbursementServiceBase = ReimbursementService(mock_dao)


def test_post_reimbursement_no_username():
    try:
        reim_service.post_reimbursement("", reim1)
        assert False
    except AccessError:
        assert True


def test_post_reimbursement_employee():
    assert reim_service.post_reimbursement(employee.get_username(), reim1)


def test_post_reimbursement_manager():
    try:
        reim_service.post_reimbursement(manager.get_username(), reim1)
        assert False
    except AccessError:
        assert True


def test_get_reimbursement_by_id_no_username():
    try:
        reim_service.get_reimbursement_by_id("", 0)
        assert False
    except AccessError:
        assert True


def test_get_reimbursement_by_id_employee():
    try:
        reim_service.get_reimbursement_by_id(employee.get_username(), 0)
        assert False
    except AccessError:
        assert True


def test_get_reimbursement_by_id_manager():
    result = reim_service.get_reimbursement_by_id(manager.get_username(), 0)
    assert result == reim1


def test_get_user_pending_reimbursement_no_username():
    try:
        reim_service.get_user_pending_reimbursement("")
        assert False
    except AccessError:
        assert True


def test_get_user_pending_reimbursement():
    assert reim_service.get_user_pending_reimbursement(employee.get_username())


def test_get_all_reimbursement_no_username():
    try:
        reim_service.get_all_reimbursement("")
        assert False
    except AccessError:
        assert True


def test_get_all_reimbursement_employee():
    try:
        reim_service.get_all_reimbursement(employee.get_username())
        assert False
    except AccessError:
        assert True


def test_get_all_reimbursement_manager():
    assert reim_service.get_all_reimbursement(manager.get_username())


def test_get_all_user_reimbursement_no_username():
    try:
        reim_service.get_all_user_reimbursement("")
        assert False
    except AccessError:
        assert True


def test_get_all_user_reimbursement_employee():
    assert reim_service.get_all_user_reimbursement(employee.get_username())


def test_get_all_user_reimbursement_manager():
    assert reim_service.get_all_user_reimbursement(manager.get_username())


def test_get_all_pending_reimbursement_no_username():
    try:
        reim_service.get_all_pending_reimbursement("")
        assert False
    except AccessError:
        assert True


def test_get_all_pending_reimbursement_employee():
    try:
        reim_service.get_all_pending_reimbursement(employee.get_username())
        assert False
    except AccessError:
        assert True


def test_get_all_pending_reimbursement_manager():
    assert reim_service.get_all_pending_reimbursement(manager.get_username())


def test_update_user_reimbursement_no_username():
    try:
        reim_service.update_user_reimbursement("", reim1)
        assert False
    except AccessError:
        assert True


def test_update_user_reimbursement_employee():
    reim_service.update_user_reimbursement(employee.get_username(), reim1)
    assert reim1.get_owner_id() == 1


def test_update_user_reimbursement_manager():
    try:
        reim_service.update_user_reimbursement(manager.get_username(), reim1)
        assert False
    except AccessError:
        assert True


def test_update_reimbursement_no_username():
    try:
        reim_service.update_reimbursement("", 0, reim1)
        assert False
    except AccessError:
        assert True


def test_update_reimbursement_employee():
    try:
        reim_service.update_reimbursement(employee.get_username(), 0, reim1)
        assert False
    except AccessError:
        assert True


def test_update_reimbursement_manager():
    reim_service.update_reimbursement(manager.get_username(), 0, reim1)
    assert reim2.get_owner_id() == 2


def test_remove_reimbursement_no_username():
    try:
        reim_service.remove_reimbursement("", 0)
        assert False
    except AccessError:
        assert True


def test_remove_reimbursement_employee():
    try:
        reim_service.remove_reimbursement(employee.get_username(), 0)
        assert False
    except AccessError:
        assert True


def test_remove_reimbursement_manager():
    assert reim_service.remove_reimbursement(manager.get_username(), 0)
