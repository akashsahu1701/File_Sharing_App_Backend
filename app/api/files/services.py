from app.api.files.repository import FileRepository


class FileService:
    def __init__(self, file_repo):
        self.file_repo: FileRepository = file_repo

    def get_file(self, file_id: int):
        return self.file_repo.get_file(file_id)

    def create_file(
        self, filename: str, file_type: str, file_data: bytes, file_size: int
    ):
        return self.file_repo.create_file(filename, file_type, file_data, file_size)

    def delete_file(self, file_id: int):
        return self.file_repo.get_file(file_id)

    def update_file(self, file_id: int, **kwargs):
        return self.file_repo.get_file(file_id)
