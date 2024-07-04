from flask_sqlalchemy import SQLAlchemy
from app.api.users.models import Settings, User, UserRole
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import func


class UserRepository:
    def __init__(self, db: SQLAlchemy):
        self.db = db

    def _serialize_user(self, user):
        return {
            "username": user.username,
            "email": user.email,
            "id": user.id,
            "created_at": user.created_at,
            "updated_at": user.updated_at,
        }

    def _serialize_settings(self, settings):
        return {
            "total_size_limits": settings.total_size_limits,
            "file_size_limit": settings.file_size_limit,
            "manage_users": settings.manage_users,
        }

    def get_user(self, username: str):
        user = (
            self.db.session.query(User)
            .filter(func.lower(User.username) == func.lower(username))
            .first()
        )

        if not user:
            return None

        return self._serialize_user(user)

    def get_user_settings(self, user_id: int):
        settings = self.db.session.query(Settings).filter_by(user_id=user_id).first()
        settings = self._serialize_settings(settings)
        return settings

    def update_settings(
        self, user_id: int, total_size: int, file_size: int, manage_users: list
    ):
        print(user_id, total_size, file_size, manage_users)
        try:
            self.db.session.query(Settings).filter_by(user_id=user_id).update(
                {
                    "total_size_limits": total_size,
                    "file_size_limit": file_size,
                    "manage_users": manage_users,
                }
            )
            self.db.session.commit()
            return True
        except SQLAlchemyError as e:
            self.db.session.rollback()
            raise e

    def create_user(
        self, username: str, email: str, password: str, role_id: int, user_ids: list
    ):
        new_user = User(username=username, email=email, password=password)
        self.db.session.add(new_user)
        try:
            self.db.session.commit()
            user_setting = Settings(
                user_id=new_user.id,
                total_size_limits=0,
                file_size_limit=0,
                manage_users=user_ids,
            )
            user_role = UserRole(user_id=new_user.id, role_id=role_id)
            try:
                self.db.session.add(user_setting)
                self.db.session.add(user_role)
                self.db.session.commit()
            except SQLAlchemyError as e:
                self.db.session.rollback()
                raise e
            return self._serialize_user(new_user)
        except SQLAlchemyError as e:
            self.db.session.rollback()
            raise e

    def update_user(self, username: str, **kwargs):
        user = self.get_user(username)
        if not user:
            return None
        for key, value in kwargs.items():
            setattr(user, key, value)
        try:
            self.db.session.commit()
            return user
        except SQLAlchemyError as e:
            self.db.session.rollback()
            raise e

    def delete_user(self, username: str):
        user = self.get_user(username)
        if not user:
            return None
        self.db.session.delete(user)
        try:
            self.db.session.commit()
            return user
        except SQLAlchemyError as e:
            self.db.session.rollback()
            raise e
