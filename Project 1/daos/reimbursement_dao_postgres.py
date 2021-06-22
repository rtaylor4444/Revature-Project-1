from typing import List
from daos.reimbursement_dao_base import ReimbursementDAOBase
from entities.reimbursement import Reimbursement
from utils.connection_util import connection
from exceptions.invalid_param_exception import InvalidParamError
from exceptions.not_found_exception import ResourceNotFoundError


class ReimbursementDAOPostgres(ReimbursementDAOBase):

    def __init__(self) -> None:
        pass

    def __create_reimbursement_from_record(self, record) -> Reimbursement:
        reimbursement = Reimbursement(record[1], record[2], record[5])
        reimbursement.set_status(2, record[3])
        reimbursement.set_owner_id(record[4])
        reimbursement.set_id(record[0])
        return reimbursement

    def __populate_list_from_records(self, records) -> List[Reimbursement]:
        reim_list: List[Reimbursement] = []
        for record in records:
            reim_list.append(self.__create_reimbursement_from_record(record))

        return reim_list

    def post_reimbursement(self, user_id: int, reim: Reimbursement) -> bool:
        # Only one pending reimbursement at a time
        try:
            self.get_user_pending_reimbursement(user_id)
            raise InvalidParamError("You can only have one pending reimbursement at once")
        except ResourceNotFoundError:
            # Add new reimbursement to the database
            sql = """insert into reimbursement (amount, reason, status, user_id, response) 
                                    values (%s,%s,%s,%s,%s) returning reimbursement_id"""
            cursor = connection.cursor()
            cursor.execute(sql, (reim.get_amount(), reim.get_reason(), 0, user_id, reim.get_response()))
            connection.commit()
            result = cursor.fetchone()
            reim.set_owner_id(user_id)
            reim.set_id(result[0])
            return True

    def get_reimbursement_by_id(self, reim_id: int) -> Reimbursement:
        sql = """select * from reimbursement where reimbursement_id = %s"""
        cursor = connection.cursor()
        cursor.execute(sql, [reim_id])
        record = cursor.fetchone()
        if record is None:
            raise ResourceNotFoundError("Reimbursement with this id does not exist")

        return self.__create_reimbursement_from_record(record)

    def get_user_pending_reimbursement(self, user_id: int) -> Reimbursement:
        sql = """select * from reimbursement where user_id = %s and status = 0"""
        cursor = connection.cursor()
        cursor.execute(sql, [user_id])
        record = cursor.fetchone()
        if record is None:
            raise ResourceNotFoundError("No pending reimbursements")

        return self.__create_reimbursement_from_record(record)

    def get_all_reimbursement(self) -> List[Reimbursement]:
        sql = """select * from reimbursement"""
        cursor = connection.cursor()
        cursor.execute(sql)
        records = cursor.fetchall()
        return self.__populate_list_from_records(records)

    def get_all_user_reimbursement(self, user_id: int) -> List[Reimbursement]:
        sql = """select * from reimbursement where user_id = %s"""
        cursor = connection.cursor()
        cursor.execute(sql, [user_id])
        records = cursor.fetchall()
        return self.__populate_list_from_records(records)

    def get_all_pending_reimbursement(self) -> List[Reimbursement]:
        sql = """select * from reimbursement where status = 0"""
        cursor = connection.cursor()
        cursor.execute(sql)
        records = cursor.fetchall()
        return self.__populate_list_from_records(records)

    def update_user_reimbursement(self, user_id: int, reim: Reimbursement) -> bool:
        # Only update the amount and reason for pending reimbursements
        sql = """update reimbursement set amount=%s, reason=%s 
                 where user_id =%s and status = 0 returning reimbursement_id"""
        cursor = connection.cursor()
        cursor.execute(sql, [reim.get_amount(), reim.get_reason(), user_id])
        connection.commit()
        record = cursor.fetchone()
        if record is None:
            raise ResourceNotFoundError("Pending reimbursement with this user id does not exist")

        reim.set_owner_id(user_id)
        reim.set_id(record[0])
        return True

    def update_reimbursement(self, reim_id: int, reim: Reimbursement) -> bool:
        # Only update the status and response
        sql = """update reimbursement set status=%s, response=%s where reimbursement_id =%s and status = 0 returning 
        user_id """
        cursor = connection.cursor()
        cursor.execute(sql, [reim.get_status(), reim.get_response(), reim_id])
        connection.commit()
        record = cursor.fetchone()
        if record is None:
            raise ResourceNotFoundError("Pending reimbursement with this user id does not exist")

        reim.set_id(reim_id)
        reim.set_owner_id(record[0])
        return True

    def remove_reimbursement(self, reim_id: int) -> bool:
        sql = """delete from reimbursement where reimbursement_id =%s returning user_id"""
        cursor = connection.cursor()
        cursor.execute(sql, [reim_id])
        connection.commit()
        record = cursor.fetchone()
        if record is None:
            raise ResourceNotFoundError("User with this id does not exist")

        return True
