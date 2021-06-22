from abc import ABC, abstractmethod
from typing import List

from entities.reimbursement import Reimbursement


class ReimbursementDAOBase(ABC):

    @abstractmethod
    def __init__(self) -> None:
        pass

    @abstractmethod
    def post_reimbursement(self, user_id: int, reim: Reimbursement) -> bool:
        pass

    @abstractmethod
    def get_reimbursement_by_id(self, reim_id: int) -> Reimbursement:
        pass

    @abstractmethod
    def get_user_pending_reimbursement(self, user_id: int) -> Reimbursement:
        pass

    @abstractmethod
    def get_all_reimbursement(self) -> List[Reimbursement]:
        pass

    @abstractmethod
    def get_all_user_reimbursement(self, user_id: int) -> List[Reimbursement]:
        pass

    @abstractmethod
    def get_all_pending_reimbursement(self) -> List[Reimbursement]:
        pass

    @abstractmethod
    def update_user_reimbursement(self, user_id: int, reim: Reimbursement) -> bool:
        pass

    @abstractmethod
    def update_reimbursement(self, reim_id: int, reim: Reimbursement) -> bool:
        pass

    @abstractmethod
    def remove_reimbursement(self, reim_id: int) -> bool:
        pass
