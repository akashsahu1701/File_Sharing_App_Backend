from io import BytesIO
from flask import Blueprint, request, send_file
from flask_jwt_extended import get_jwt_identity, jwt_required
from app import db
from werkzeug.utils import secure_filename

from app.api.files.repository import FileRepository
from app.api.files.services import FileService
from app.api.users.repository import UserRepository
from app.responses.response import send_response


files_api = Blueprint("files_api", "files_api", url_prefix="/api/files")
file_repo = FileRepository(db)
user_repo = UserRepository(db)
file_service = FileService(file_repo, user_repo)


@files_api.get("/me")
@jwt_required()
def get_my_files():
    user_id = get_jwt_identity()
    files = file_service.get_my_files(user_id=user_id)
    return send_response(data=files, message="Files retrieved", status_code=200), 200


@files_api.get("/<file_id>")
@jwt_required()
def get_files(file_id: str):
    user_id = get_jwt_identity()
    file = file_service.get_file(file_id=int(file_id), user_id=int(user_id))
    if not file:
        return (
            send_response(
                data={},
                message="You do not have permission to access this resource",
                status_code=403,
                error="Forbidden",
            ),
            403,
        )
    file_data = BytesIO(file.data)
    return send_file(
        file_data,
        mimetype=file.file_type,
        download_name=file.name,
        as_attachment=False,
    )


@files_api.post("/")
@jwt_required()
def create_file():
    try:
        if "file" not in request.files:
            return (
                send_response(
                    data={}, message="Bad request", status_code=400, error="No file"
                ),
                400,
            )

        created_by = get_jwt_identity()
        file = request.files["file"]
        filename = secure_filename(file.filename)
        file_data = file.read()
        file_type = file.content_type
        file_size = len(file_data)

        if not file_service.isValidFile(user_id=created_by, file_size=len(file_data)):
            return (
                send_response(
                    data={},
                    message="Bad request",
                    status_code=400,
                    error="File too large",
                ),
                400,
            )

        file_service.create_file(
            filename=filename,
            file_type=file_type,
            file_data=file_data,
            file_size=file_size,
            created_by=created_by,
        )
        return send_response(data={}, message="File created", status_code=201), 201

    except Exception as e:
        return (
            send_response(
                data={}, message="Bad request", status_code=400, error=str(e)
            ),
            400,
        )
