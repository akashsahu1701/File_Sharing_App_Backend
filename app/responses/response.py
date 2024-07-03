from flask import jsonify
from typing import Any

class DatabaseError(Exception):
    pass


def handle_database_error(error):
    response = jsonify({"error": error})
    response.status_code = 500
    return response


def get_status(status_code: int):
    if status_code >= 100 and status_code < 200:
        return "Informational"
    elif status_code >= 200 and status_code < 300:
        return "Success"
    elif status_code >= 300 and status_code < 400:
        return "Redirection"
    elif status_code >= 400 and status_code < 500:
        return "Client Error"
    elif status_code >= 500 and status_code < 600:
        return "Server Error"
    else:
        return "Unknown"


def send_response(data: dict, message: str, status_code: int = 200, error: Any = None):
    return jsonify(
        {
            "data": data,
            "msg": message,
            "error": error,
            "code": status_code,
            "status": get_status(status_code),
        }
    )
