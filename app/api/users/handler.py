from flask import Blueprint, request, jsonify
from app import db
from app.api.users.repository import UserRepository
from app.api.users.schema import UserSchema
from app.api.users.services import UserService
from app.responses.response import send_response

users_api = Blueprint("users_api", "users_api", url_prefix="/api/users")
user_repo = UserRepository(db)
user_service = UserService(user_repo)


@users_api.route("/<username>", methods=["GET"])
def get_user(username: str):
    try:
        user = user_service.get_user(username)
        if user is None:
            return (
                send_response(
                    data={},
                    message="User not found",
                    error=None,
                    status_code=404,
                ),
                404,
            )
        return (
            send_response(
                data=user,
                message="User fetched successfully",
                error=None,
                status_code=200,
            ),
            200,
        )
    except Exception as e:
        return (
            send_response(
                data={},
                message="Bad Request",
                status_code=400,
                error=str(e),
            ),
            404,
        )


@users_api.route("/", methods=["POST"])
def create_user():
    data = request.json
    data = UserSchema(**data)
    try:
        user = user_service.create_user(data.username, data.email, data.password)
        return (
            send_response(
                data=user, message="User created", error=None, status_code=201
            ),
            201,
        )
    except Exception as e:
        return (
            send_response(
                data={}, message="bad request", error=str(e), status_code=400
            ),
            400,
        )


@users_api.route("/<username>", methods=["PUT"])
def update_user(username):
    data = request.json
    try:
        user = user_service.update_user(username, **data)
        if not user:
            return send_response(
                data={},
                message="User not found",
                status_code=404,
                error="User not found",
            )
        return (
            send_response(
                data={"username": user.username, "email": user.email},
                message="User updated",
                status_code=200,
                error=None,
            ),
            200,
        )
    except Exception as e:
        return (
            send_response(
                data={}, message="bad request", status_code=400, error=str(e)
            ),
            400,
        )


@users_api.route("/<username>", methods=["DELETE"])
def delete_user(username):
    try:
        user = user_service.delete_user(username)
        if not user:
            return (
                send_response(
                    data={}, message="User not found", error=None, status_code=404
                ),
                404,
            )
        return jsonify({"message": "User deleted"})
    except Exception as e:
        return (
            send_response(
                data={}, message="bad request", error=str(e), status_code=400
            ),
            400,
        )
