from typing import List
from services.reimbursement_service_base import ReimbursementServiceBase
from daos.reimbursement_dao_base import ReimbursementDAOBase
from entities.reimbursement import Reimbursement
from services.login_manager import login_manager
from exceptions.access_exception import AccessError


class ReimbursementService(ReimbursementServiceBase):

    def __init__(self, reim_dao: ReimbursementDAOBase):
        self.__reim_dao = reim_dao

    def post_reimbursement(self, username: str, reim: Reimbursement) -> bool:
        if login_manager.get_user_role(username) == 1:
            return self.__reim_dao.post_reimbursement(login_manager.get_user_id(username), reim)
        else:
            raise AccessError("Only employees can post reimbursement requests")

    def get_reimbursement_by_id(self, username: str, reim_id: int) -> Reimbursement:
        if login_manager.get_user_role(username) & 2 != 0:
            return self.__reim_dao.get_reimbursement_by_id(reim_id)
        else:
            raise AccessError("Access Denied")

    def get_user_pending_reimbursement(self, username: str) -> Reimbursement:
        return self.__reim_dao.get_user_pending_reimbursement(login_manager.get_user_id(username))

    def get_all_reimbursement(self, username: str) -> List[Reimbursement]:
        if login_manager.get_user_role(username) & 2 != 0:
            return self.__reim_dao.get_all_reimbursement()
        else:
            raise AccessError("Access Denied")

    def get_all_user_reimbursement(self, username: str) -> List[Reimbursement]:
        return self.__reim_dao.get_all_user_reimbursement(login_manager.get_user_id(username))

    def get_all_pending_reimbursement(self, username: str) -> List[Reimbursement]:
        if login_manager.get_user_role(username) & 2 != 0:
            return self.__reim_dao.get_all_pending_reimbursement()
        else:
            raise AccessError("Access Denied")

    def update_user_reimbursement(self, username: str, reim: Reimbursement) -> bool:
        if login_manager.get_user_role(username) == 1:
            return self.__reim_dao.update_user_reimbursement(login_manager.get_user_id(username), reim)
        else:
            raise AccessError("Only employees can update their reimbursement details")

    def update_reimbursement(self, username: str, reim_id: int, reim: Reimbursement) -> bool:
        if login_manager.get_user_role(username) & 2 != 0:
            return self.__reim_dao.update_reimbursement(reim_id, reim)
        else:
            raise AccessError("Access Denied")

    def remove_reimbursement(self, username: str, reim_id: int) -> bool:
        if login_manager.get_user_role(username) & 2 != 0:
            return self.__reim_dao.remove_reimbursement(reim_id)
        else:
            raise AccessError("Access Denied")
