from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import and_
from app.api.files.models import File, FilePermission


class FileRepository:
    def __init__(self, db: SQLAlchemy):
        self.db = db

    def _serialize_file(self, file):
        return {
            "id": file.id,
            "name": file.name,
            "file_type": file.file_type,
            "size": file.size,
        }

    def get_file(self, file_id: int, user_id: int):
        file = (
            self.db.session.query(File)
            .join(
                FilePermission,
                and_(
                    File.id == FilePermission.file_id,
                    FilePermission.user_id == user_id,
                    FilePermission.can_view == True,
                ),
            )
            .filter(File.id == file_id)
            .first()
        )

        if not file:
            return None
        return file

    def get_my_files(self, user_id: int):
        files = (
            self.db.session.query(File)
            .join(
                FilePermission,
                and_(
                    File.id == FilePermission.file_id,
                    FilePermission.user_id == user_id,
                    FilePermission.can_view == True,
                ),
            )
            .all()
        )

        files = [self._serialize_file(file) for file in files]

        return files

    def create_file(
        self,
        filename: str,
        file_type: str,
        file_data: bytes,
        file_size: int,
        created_by: str,
    ):
        new_file = File(
            name=filename,
            file_type=file_type,
            size=file_size,
            data=file_data,
        )
        self.db.session.add(new_file)
        try:
            self.db.session.commit()
            file_id = new_file.id  # Retrieve the ID after committing
        except SQLAlchemyError as e:
            self.db.session.rollback()
            raise e

        file_permissions = FilePermission(
            file_id=file_id,  # Use the retrieved ID here
            user_id=created_by,
            can_edit=True,
            can_view=True,
        )
        self.db.session.add(file_permissions)
        try:
            self.db.session.commit()
            return new_file
        except SQLAlchemyError as e:
            self.db.session.rollback()
            raise e
