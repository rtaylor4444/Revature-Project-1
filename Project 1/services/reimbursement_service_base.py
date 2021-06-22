from abc import ABC, abstractmethod
from typing import List
from entities.reimbursement import Reimbursement


class ReimbursementServiceBase(ABC):

    @abstractmethod
    def post_reimbursement(self, username: str, reim: Reimbursement) -> bool:
        pass

    @abstractmethod
    def get_reimbursement_by_id(self, username: str, reim_id: int) -> Reimbursement:
        pass

    @abstractmethod
    def get_user_pending_reimbursement(self, username: str) -> Reimbursement:
        pass

    @abstractmethod
    def get_all_reimbursement(self, username: str) -> List[Reimbursement]:
        pass

    @abstractmethod
    def get_all_user_reimbursement(self, username: str) -> List[Reimbursement]:
        pass

    @abstractmethod
    def get_all_pending_reimbursement(self, username: str) -> List[Reimbursement]:
        pass

    @abstractmethod
    def update_user_reimbursement(self, username: str, reim: Reimbursement) -> bool:
        pass

    @abstractmethod
    def update_reimbursement(self, username: str, reim_id: int, reim: Reimbursement) -> bool:
        pass

    @abstractmethod
    def remove_reimbursement(self, username: str, reim_id: int) -> bool:
        pass
