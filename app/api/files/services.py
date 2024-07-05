from app.api.files.repository import FileRepository
from app.api.users.repository import UserRepository


class FileService:
    def __init__(self, file_repo, user_repo):
        self.file_repo: FileRepository = file_repo
        self.user_repo: UserRepository = user_repo

    def get_file(self, file_id: int, user_id: int):
        return self.file_repo.get_file(file_id, user_id)

    def get_my_files(self, user_id: int):
        return self.file_repo.get_my_files(user_id)

    def isValidFile(self, user_id: int, file_size: int):
        users_settings = self.user_repo.get_user_settings(user_id)
        print(file_size, users_settings["file_size_limit"])
        if users_settings["file_size_limit"] * 1024 < file_size:
            return False
        return True

    def create_file(
        self,
        filename: str,
        file_type: str,
        file_data: bytes,
        file_size: int,
        created_by: str,
    ):
        return self.file_repo.create_file(
            filename, file_type, file_data, file_size, created_by
        )

    def get_users_access_to_file(self, file_id: int):
        return self.file_repo.get_users_access_to_file(file_id)

    def give_access_to_user(
        self, file_id: int, user_id: int, can_view: bool | None, can_edit: bool | None
    ):
        return self.file_repo.give_access_to_user(file_id, user_id, can_view, can_edit)

    def delete_file(self, file_id: int):
        return self.file_repo.delete_file(file_id)

    def update_file(self, file_id: int, **kwargs):
        return self.file_repo.get_file(file_id)
