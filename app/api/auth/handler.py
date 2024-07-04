from flask import Blueprint, request
from app import db

from app.api.auth.repository import AuthRepository
from app.api.auth.schema import LoginSchema
from app.api.auth.services import AuthService
from app.responses.response import send_response


auth_api = Blueprint("auth_api", "auth_api", url_prefix="/api/auth")
auth_repo = AuthRepository(db)
auth_service = AuthService(auth_repo)


@auth_api.post("/login")
def login():
    try:
        data = request.json
        data = LoginSchema(**data)
        user, token = auth_service.login(data.username, data.password)
        if not user:
            return (
                send_response(
                    data={}, message="User not found", error=None, status_code=404
                ),
                404,
            )

        if not token:
            return (
                send_response(
                    data={}, message="Invalid credentials", error=None, status_code=401
                ),
                401,
            )
        return (
            send_response(
                data={"token": token, "user": user},
                message="Login successful",
                status_code=200,
            ),
            200,
        )
    except Exception as e:
        return (
            send_response(
                data={}, message="bad request", error=str(e), status_code=400
            ),
            400,
        )
