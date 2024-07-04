from io import BytesIO
from flask import Blueprint, request, send_file
from app import db
from werkzeug.utils import secure_filename

from app.api.files.repository import FileRepository
from app.api.files.services import FileService
from app.responses.response import send_response


files_api = Blueprint("files_api", "files_api", url_prefix="/api/files")
file_repo = FileRepository(db)
file_service = FileService(file_repo)


@files_api.get("/<file_id>")
def get_files(file_id: str):
    file = file_service.get_file(file_id=int(file_id))
    file_data = BytesIO(file.data)
    return send_file(
        file_data,
        mimetype=file.file_type,
        download_name=file.name,
        as_attachment=False,
    )


@files_api.post("/")
def create_file():
    try:
        file = request.files["file"]
        filename = secure_filename(file.filename)
        file_data = file.read()
        file_type = file.content_type
        file_size = len(file_data)
        print(file.filename, file_type, file_size)

        file_service.create_file(
            filename=filename,
            file_type=file_type,
            file_data=file_data,
            file_size=file_size,
        )
        return send_response(data={}, message="File created", status_code=201), 201

    except Exception as e:
        return (
            send_response(
                data={}, message="Bad request", status_code=400, error=str(e)
            ),
            400,
        )
