from datetime import timedelta
from flask_jwt_extended import create_access_token
from flask_sqlalchemy import SQLAlchemy
from app.api.users.models import RolePermission, User, UserRole
from app.utils.password import verify_password


class AuthRepository:
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

    def generate_access_token(self, user_id: str, data) -> str:
        token = create_access_token(
            identity=user_id,
            additional_claims={"data": data},
            expires_delta=timedelta(days=5),
        )
        return token

    def login(self, username: str, password: str):
        user = self.db.session.query(User).filter_by(username=username).first()
        if not user:
            return None, None

        isVerified = verify_password(user.password, password)

        user_roles = self.db.session.query(UserRole).filter_by(user_id=user.id).all()
        role_id = user_roles[0].role_id
        user_permissions = (
            self.db.session.query(RolePermission).filter_by(role_id=role_id).all()
        )

        permission_id = user_permissions[0].permission_id

        if isVerified:
            return self._serialize_user(user), self.generate_access_token(
                user.id, data={"role_id": role_id, "permission_id": permission_id}
            )
        return self._serialize_user(user), None
