from typing import Optional
from pydantic import BaseModel


class UserSchema(BaseModel):
    username: str
    email: str
    password: str
    role_id: int
    user_ids: list


class UpdateUserSettingsSchema(BaseModel):
    user_id: int
    total_size_limits: int
    file_size_limit: int
    manage_users: Optional[list] = None
