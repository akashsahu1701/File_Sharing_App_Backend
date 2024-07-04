from app.api.users.repository import UserRepository
from sqlalchemy.exc import SQLAlchemyError

from app.utils.password import hash_password


class UserService:
    def __init__(self, repository: UserRepository):
        self.repository = repository

    def get_user(self, username: str):
        return self.repository.get_user(username)

    def create_user(self, username: str, email: str, password_hash: str):
        try:
            encrypted_password = hash_password(password_hash)
            return self.repository.create_user(username, email, encrypted_password)
        except SQLAlchemyError as e:
            raise Exception(f"Error creating user: {str(e)}")

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
