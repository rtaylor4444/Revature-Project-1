from exceptions.invalid_param_exception import InvalidParamError


class Reimbursement:

    def __init__(self, amount: int = 0, reason: str = "", response: str = ""):
        self.__id = 0
        self.__amount = amount
        self.__reason = reason
        self.__owner_id = 0
        self.__status = 0
        self.__response = response

    def get_amount(self) -> int:
        return self.__amount

    def get_reason(self) -> str:
        return self.__reason

    def get_response(self) -> str:
        return self.__response

    def get_id(self) -> int:
        return self.__id

    def get_owner_id(self) -> int:
        return self.__owner_id

    def get_status(self) -> int:
        return self.__status

    def is_approved(self) -> bool:
        return self.__status == 1

    def is_pending(self) -> bool:
        return self.__status == 0

    def is_denied(self) -> bool:
        return self.__status == -1

    def set_id(self, new_id: int) -> bool:
        if self.__id != 0:
            return False

        self.__id = new_id
        return True

    def set_owner_id(self, new_id: int) -> bool:
        if self.__owner_id != 0:
            return False

        self.__owner_id = new_id
        return True

    def set_status(self, incoming_role: int, new_status: int) -> bool:
        # Can only update if a manager or pending
        if self.__status != 0 or incoming_role & 2 == 0:
            return False
        if new_status < -1 or new_status > 1:
            return False

        self.__status = new_status
        return True

    def set_response(self, incoming_role: int, new_response: str) -> bool:
        # Can only update if a manager or pending
        if incoming_role & 2 == 0:
            return False

        self.__response = new_response
        return True

    def to_json_dict(self):
        return {
            "id": self.__id,
            "amount": self.__amount,
            "reason": self.__reason,
            "owner": self.__owner_id,
            "status": self.__status,
            "response": self.__response
        }

    def set_from_json(self, incoming_role: int, json: dict):
        amount = json.get("amount")
        if amount is None:
            raise InvalidParamError("amount param missing")
        elif not str(amount).isdigit():
            raise InvalidParamError("amount must be a number!")

        reason = json.get("reason")
        if reason is None:
            raise InvalidParamError("reason param missing")

        owner = json.get("owner")
        if owner is None:
            raise InvalidParamError("owner param missing")
        elif not str(owner).isdigit():
            raise InvalidParamError("owner id must be a number!")

        status = json.get("status")
        if status is not None:
            if not str(status).lstrip("-").isdigit():
                raise InvalidParamError("status must be a number")
            if not self.set_status(incoming_role, int(status)):
                raise InvalidParamError("status must either -1, 0 or 1")

        response = json.get("response")
        if response is not None:
            self.set_response(incoming_role, str(response))

        self.__amount = int(amount)
        self.__reason = str(reason)
        self.__owner_id = int(owner)
