from app.api.auth.repository import AuthRepository


class AuthService:
    def __init__(self, repository: AuthRepository):
        self.repository = repository

    def login(self, username: str, password: str):
        return self.repository.login(username, password)
