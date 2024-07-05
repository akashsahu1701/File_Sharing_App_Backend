from datetime import timedelta
from flask_jwt_extended import create_access_token
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import joinedload

from app.api.users.models import Permission, RolePermission, User, UserRole
from app.utils.password import verify_password


class AuthRepository:
    def __init__(self, db: SQLAlchemy):
        self.db = db

    def _serialize_user(self, user):
        roles = [role.name for role in user.roles]
        return {
            "username": user.username,
            "email": user.email,
            "id": user.id,
            "created_at": user.created_at,
            "updated_at": user.updated_at,
            "roles": roles[0],
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

        is_verified = verify_password(user.password, password)

        query = (
            self.db.session.query(User, UserRole, RolePermission)
            .filter(User.id == user.id)
            .outerjoin(UserRole, UserRole.user_id == User.id)
            .outerjoin(RolePermission, RolePermission.role_id == UserRole.role_id)
            .outerjoin(Permission, Permission.id == RolePermission.permission_id)
            .options(joinedload(User.roles))
        )

        user_permissions = []

        # Execute the query
        results = query.all()

        if not results:
            return None, None

        user_roles = [role.role_id for _, role, _ in results if role]
        user_permissions = [perm.permission_id for _, _, perm in results if perm]

        # Generate access token if verified
        if is_verified:
            return self._serialize_user(user), self.generate_access_token(
                user.id, data={"roles": user_roles, "permissions": user_permissions}
            )
        return self._serialize_user(user), None
