from app.api.users.repository import UserRepository
from sqlalchemy.exc import SQLAlchemyError

from app.utils.password import hash_password


class UserService:
    def __init__(self, repository: UserRepository):
        self.repository = repository

    def get_user(self, username: str):
        return self.repository.get_user(username)

    def create_user(
        self,
        username: str,
        email: str,
        password_hash: str,
        role_id: int,
        user_ids: list,
    ):
        try:
            encrypted_password = hash_password(password_hash)
            return self.repository.create_user(
                username, email, encrypted_password, role_id, user_ids
            )
        except SQLAlchemyError as e:
            raise Exception(f"Error creating user: {str(e)}")

    def get_user_settings(self, user_id: int):
        return self.repository.get_user_settings(user_id)

    def update_user_settings(
        self, user_id: int, total_size: int, file_size: int, manage_users: list
    ):
        return self.repository.update_settings(
            user_id, total_size, file_size, manage_users
        )

    def update_user(self, username: str, **kwargs):
        try:
            return self.repository.update_user(username, **kwargs)
        except SQLAlchemyError as e:
            raise Exception(f"Error updating user: {str(e)}")

    def delete_user(self, username: str):
        try:
            return self.repository.delete_user(username)
        except SQLAlchemyError as e:
            raise Exception(f"Error deleting user: {str(e)}")
