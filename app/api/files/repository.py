from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import and_

# from moviepy.editor import VideoFileClip
from app.api.files.models import File, FilePermission
from app.api.users.models import User


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
        # file = (
        #     self.db.session.query(File)
        #     .join(
        #         FilePermission,
        #         and_(
        #             File.id == FilePermission.file_id,
        #             FilePermission.user_id == user_id,
        #             FilePermission.can_view == True,
        #         ),
        #     )
        #     .filter(File.id == file_id)
        #     .first()
        # )

        file = self.db.session.query(File).filter(File.id == file_id).first()

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

    # def trim_video(self, file_id, start_time, end_time):
    #     file = self.db.session.query(File).filter(File.id == file_id).first()
    #     clip = VideoFileClip(file.data)
    #     trimmed_clip = clip.subclip(start_time, end_time)
    #     return trimmed_clip

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

    def get_users_access_to_file(self, file_id: int):
        users = self.db.session.query(User.username, User.id).all()

        users_access = (
            self.db.session.query(FilePermission)
            .filter(FilePermission.file_id == file_id)
            .all()
        )

        users_with_access = []
        for username, user_id in users:
            user_info = {
                "id": user_id,
                "username": username,
                "can_view": False,
                "can_edit": False,
            }
            for access in users_access:
                if access.user_id == user_id:
                    user_info["can_view"] = access.can_view
                    user_info["can_edit"] = access.can_edit
                    break  # No need to check further if found
            users_with_access.append(user_info)

        return users_with_access

    def give_access_to_user(
        self, file_id: int, user_id: int, can_view: bool | None, can_edit: bool | None
    ):
        try:
            file_permission = (
                self.db.session.query(FilePermission)
                .filter_by(file_id=file_id, user_id=user_id)
                .first()
            )

            if file_permission:
                if can_view is not None:
                    file_permission.can_view = can_view
                if can_edit is not None:
                    file_permission.can_edit = can_edit
            else:
                file_permission = FilePermission(
                    file_id=file_id,
                    user_id=user_id,
                    can_view=can_view if can_view is not None else False,
                    can_edit=can_edit if can_edit is not None else False,
                )
                self.db.session.add(file_permission)

            self.db.session.commit()
            return True
        except SQLAlchemyError as e:
            self.db.session.rollback()
            raise e

    def delete_file(self, file_id: int):
        self.db.session.query(FilePermission).filter(
            FilePermission.file_id == file_id
        ).delete()
        self.db.session.query(File).filter(File.id == file_id).delete()
        try:
            self.db.session.commit()
            return True
        except SQLAlchemyError as e:
            self.db.session.rollback()
            raise e
