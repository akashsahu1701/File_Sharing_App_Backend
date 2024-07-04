from app.api.files.repository import FileRepository


class FileService:
    def __init__(self, file_repo):
        self.file_repo: FileRepository = file_repo

    def get_file(self, file_id: int, user_id: int):
        return self.file_repo.get_file(file_id, user_id)

    def get_my_files(self, user_id: int):
        return self.file_repo.get_my_files(user_id)

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

    def delete_file(self, file_id: int):
        return self.file_repo.get_file(file_id)

    def update_file(self, file_id: int, **kwargs):
        return self.file_repo.get_file(file_id)
