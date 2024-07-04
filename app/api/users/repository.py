from flask_sqlalchemy import SQLAlchemy
from app.api.users.models import User
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

    def get_user(self, username: str):
        user = (
            self.db.session.query(User)
            .filter(func.lower(User.username) == func.lower(username))
            .first()
        )

        if not user:
            return None

        return self._serialize_user(user)

    def create_user(self, username: str, email: str, password: str):
        new_user = User(username=username, email=email, password=password)
        self.db.session.add(new_user)
        try:
            self.db.session.commit()
            return new_user
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
