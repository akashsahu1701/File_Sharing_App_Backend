from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import SQLAlchemyError
from app.api.files.models import File


class FileRepository:
    def __init__(self, db: SQLAlchemy):
        self.db = db

    def get_file(self, file_id: int):
        file = self.db.session.query(File).filter_by(id=file_id).first()
        if not file:
            return None
        return file

    def create_file(
        self, filename: str, file_type: str, file_data: bytes, file_size: int
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
            return new_file
        except SQLAlchemyError as e:
            self.db.session.rollback()
            raise e
