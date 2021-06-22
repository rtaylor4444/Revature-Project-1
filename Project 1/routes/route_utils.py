from flask import Flask, request, jsonify
from exceptions.invalid_param_exception import InvalidParamError


def fetch_request_body():
    body = request.json
    if body is None:
        raise InvalidParamError("You have submitted an empty form try again!")
    return body


def get_incoming_username() -> str:
    username: str = request.headers.get("username")
    if username is None:
        username = ""
    return username


def get_id_from_string(type_id: str) -> int:
    if not type_id.isdigit():
        return -1
    else:
        return int(type_id)
