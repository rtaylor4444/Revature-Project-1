from flask import Flask, request, jsonify
from routes.route_utils import fetch_request_body, get_incoming_username, get_id_from_string
from services.user_service_base import UserServiceBase
from services.user_service import UserService
from services.login_manager import login_manager
from daos.user_dao_base import UserDAOBase
from daos.user_dao_postgres import UserDAOPostgres
from entities.user import User
from exceptions.invalid_param_exception import InvalidParamError
from exceptions.not_found_exception import ResourceNotFoundError
from exceptions.access_exception import AccessError

user_service: UserServiceBase = UserService(UserDAOPostgres())


def create_user_routes(app: Flask):
    def get_incoming_role_safe(username: str) -> int:
        try:
            return login_manager.get_user_role(username)
        except AccessError:
            return 1

    @app.route("/users/new", methods=["POST"])
    def create_user():
        try:
            # Managers can make other managers
            username: str = get_incoming_username()
            incoming_role: int = get_incoming_role_safe(username)

            user: User = User()
            user.set_from_json(incoming_role, fetch_request_body())
            user_service.post_user(username, user)
            return jsonify(user.to_json_dict()), 201
        except InvalidParamError as e:
            return e.message, 400
        except AccessError as e:
            return e.message, 403

    @app.route("/users/login", methods=["POST"])
    def login():
        try:
            body = fetch_request_body()
            user: User = user_service.login(body.get("username"), body.get("password"))
            return user.to_json_dict(), 200
        except ResourceNotFoundError as e:
            return e.message, 404
        except InvalidParamError as e:
            return e.message, 400
        except AccessError as e:
            return e.message, 403

    @app.route("/users/logout", methods=["POST"])
    def logout():
        username: str = get_incoming_username()
        user_service.logout(username)
        return "Successfully logged out", 200

    @app.route("/users/<user_id>", methods=["GET"])
    def get_user(user_id: str):
        try:
            username: str = get_incoming_username()
            converted_id: int = get_id_from_string(user_id)
            user: User = user_service.get_user(username, converted_id)
            return jsonify(user.to_json_dict()), 200
        except ResourceNotFoundError as e:
            return e.message, 404
        except AccessError as e:
            return e.message, 403
