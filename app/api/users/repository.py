from flask_sqlalchemy import SQLAlchemy
from app.api.users.models import Permission, Settings, User, UserRole
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import func
from sqlalchemy.orm import joinedload


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

    def get_users(self, user_id: int, permissions: list[int]):
        permission = (
            self.db.session.query(Permission)
            .filter(Permission.id.in_(permissions))
            .first()
        )

        query = (
            self.db.session.query(User)
            .options(joinedload(User.settings))
            .options(joinedload(User.roles))
        )
        users = []

        if permission.name == "manage_all_accounts":
            users = query.all()
        elif permission.name == "manage_set_of_accounts":
            settings = (
                self.db.session.query(Settings).filter_by(user_id=user_id).first()
            )
            manage_users = settings.manage_users
            users = query.filter(User.id.in_(manage_users)).all()

            print(users)
        result = []
        for user in users:
            user = {
                **self._serialize_user(user),
                **self._serialize_settings(user.settings),
                "role": user.roles[0].name,
            }
            result.append(user)

        return result

    def get_user_settings(self, user_id: int):
        settings = self.db.session.query(Settings).filter_by(user_id=user_id).first()
        settings = self._serialize_settings(settings)
        return settings

    def update_settings(
        self, user_id: int, total_size: int, file_size: int, manage_users: list | None
    ):
        print(user_id, total_size, file_size, manage_users)
        try:
            query = self.db.session.query(Settings).filter_by(user_id=user_id)
            if manage_users:
                query.update(
                    {
                        "total_size_limits": total_size,
                        "file_size_limit": file_size,
                        "manage_users": manage_users,
                    }
                )
            else:
                query.update(
                    {
                        "total_size_limits": total_size,
                        "file_size_limit": file_size,
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
            if role_id == 2:
                user_ids.append(new_user.id)
            user_setting = Settings(
                user_id=new_user.id,
                total_size_limits=100,
                file_size_limit=100,
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
            if "username" in str(e.orig):
                raise ValueError("Username already exists")
            elif "email" in str(e.orig):
                raise ValueError("Email already exists")
            else:
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
