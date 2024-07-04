from flask import Blueprint, request, jsonify
from app import db
from app.api.users.repository import UserRepository
from app.api.users.schema import UpdateUserSettingsSchema, UserSchema
from app.api.users.services import UserService
from app.responses.response import send_response

users_api = Blueprint("users_api", "users_api", url_prefix="/api/users")
user_repo = UserRepository(db)
user_service = UserService(user_repo)


@users_api.get("/<username>")
def get_user(username: str):
    try:
        user = user_service.get_user(username)
        user_settings = user_service.get_user_settings(user_id=user["id"])
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
                data={**user, **user_settings},
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


@users_api.post("/")
def create_user():
    data = request.json
    data = UserSchema(**data)
    try:
        user = user_service.create_user(
            data.username, data.email, data.password, data.role_id, data.user_ids
        )
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


@users_api.put("/settings")
def update_user_settings():
    data = request.json
    settings = UpdateUserSettingsSchema(**data)
    try:
        user = user_service.update_user_settings(
            settings.user_id,
            settings.total_size_limits,
            settings.file_size_limit,
            settings.manage_users,
        )
        if not user:
            return send_response(
                data={},
                message="User not found",
                status_code=404,
                error="User not found",
            )
        return (
            send_response(
                data={},
                message="User settings updated successfully",
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


@users_api.put("/<username>")
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


@users_api.delete("/<username>")
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
