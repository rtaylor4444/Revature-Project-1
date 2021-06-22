from typing import List
from flask import Flask, request, jsonify
from routes.route_utils import fetch_request_body, get_incoming_username, get_id_from_string
from services.reimbursement_service_base import ReimbursementServiceBase
from services.reimbursement_service import ReimbursementService
from services.login_manager import login_manager
from daos.reimbursement_dao_base import ReimbursementDAOBase
from daos.reimbursement_dao_postgres import ReimbursementDAOPostgres
from entities.reimbursement import Reimbursement
from exceptions.invalid_param_exception import InvalidParamError
from exceptions.not_found_exception import ResourceNotFoundError
from exceptions.access_exception import AccessError

reim_service: ReimbursementServiceBase = ReimbursementService(ReimbursementDAOPostgres())


def create_reimbursement_routes(app: Flask):

    @app.route("/reimbursements/new", methods=["POST"])
    def post_reimbursement():
        try:
            username: str = get_incoming_username()
            incoming_role: int = login_manager.get_user_role(username)
            reim: Reimbursement = Reimbursement()
            reim.set_from_json(incoming_role, fetch_request_body())
            reim_service.post_reimbursement(username, reim)
            return jsonify(reim.to_json_dict()), 201
        except InvalidParamError as e:
            return e.message, 400
        except AccessError as e:
            return e.message, 403

    @app.route("/reimbursements/me", methods=["GET"])
    def get_user_pending_reimbursement():
        try:
            username: str = get_incoming_username()
            reim: Reimbursement = reim_service.get_user_pending_reimbursement(username)
            return jsonify(reim.to_json_dict()), 200
        except AccessError as e:
            return e.message, 403
        except ResourceNotFoundError as e:
            return e.message, 404

    @app.route("/reimbursements", methods=["GET"])
    def get_all_reimbursement():
        try:
            username: str = get_incoming_username()
            reim_list: List[Reimbursement] = reim_service.get_all_reimbursement(username)
            json_reims = [r.to_json_dict() for r in reim_list]
            return jsonify(json_reims), 200
        except AccessError as e:
            return e.message, 403

    @app.route("/reimbursements/all", methods=["GET"])
    def get_all_user_reimbursement():
        try:
            username: str = get_incoming_username()
            reim_list: List[Reimbursement] = reim_service.get_all_user_reimbursement(username)
            json_reims = [r.to_json_dict() for r in reim_list]
            return jsonify(json_reims), 200
        except AccessError as e:
            return e.message, 403

    @app.route("/reimbursements/pending", methods=["GET"])
    def get_all_pending_reimbursement():
        try:
            username: str = get_incoming_username()
            reim_list: List[Reimbursement] = reim_service.get_all_pending_reimbursement(username)
            json_reims = [r.to_json_dict() for r in reim_list]
            return jsonify(json_reims), 200
        except AccessError as e:
            return e.message, 403

    @app.route("/reimbursements/update/me", methods=["PUT"])
    def update_user_pending_reimbursement():
        try:
            username: str = get_incoming_username()
            incoming_role: int = login_manager.get_user_role(username)
            reim: Reimbursement = Reimbursement()
            reim.set_from_json(incoming_role, fetch_request_body())
            reim_service.update_user_reimbursement(username, reim)
            return jsonify(reim.to_json_dict()), 200
        except InvalidParamError as e:
            return e.message, 400
        except AccessError as e:
            return e.message, 403
        except ResourceNotFoundError as e:
            return e.message, 404

    @app.route("/reimbursements/update/<reim_id>", methods=["PUT"])
    def update_reimbursement(reim_id: str):
        try:
            username: str = get_incoming_username()
            incoming_role: int = login_manager.get_user_role(username)
            converted_id: int = get_id_from_string(reim_id)
            reim: Reimbursement = Reimbursement()
            reim.set_from_json(incoming_role, fetch_request_body())
            reim_service.update_reimbursement(username, converted_id, reim)
            return jsonify(reim.to_json_dict()), 200
        except InvalidParamError as e:
            return e.message, 400
        except AccessError as e:
            return e.message, 403
        except ResourceNotFoundError as e:
            return e.message, 404
